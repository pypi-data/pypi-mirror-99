import decimal
from decimal import Decimal, Context
from typing import Any, List


class Utils:
    TYPE_STRING = 'S'
    TYPE_NUMBER = 'N'
    TYPE_BINARY = 'B'
    TYPE_STRING_SET = 'SS'
    TYPE_NUMBER_SET = 'NS'
    TYPE_BINARY_SET = 'BS'
    TYPE_NULL = 'NULL'
    TYPE_BOOLEAN = 'BOOL'
    TYPE_MAP = 'M'
    TYPE_LIST = 'L'
    ALL_TYPES_WHERE_VALUE_DO_NOT_NEED_MODIFICATIONS = [TYPE_STRING, TYPE_BOOLEAN]

    DECIMAL_DYNAMODB_CONTEXT = Context(prec=38, rounding=decimal.ROUND_HALF_EVEN, Emin=-128, Emax=126,
                                       capitals=1, clamp=0, flags=[], traps=[])
    # 38 is the maximum numbers of Decimals numbers that DynamoDB can support.

    from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
    # The serializer and deserializer can be static, even in a lambda,
    # since their classes will never change according to the user.
    _serializer = None
    _deserializer = None

    @classmethod
    def serializer(cls) -> TypeSerializer:
        if cls._serializer is None:
            cls._serializer = cls.TypeSerializer()
        return cls._serializer
    
    @classmethod
    def deserializer(cls) -> TypeDeserializer:
        if cls._deserializer is None:
            cls._deserializer = cls.TypeDeserializer()
        return cls._deserializer

    # todo: deprecate this function that was a complication because i was using the decimal module
    @staticmethod
    def float_serializer(python_object):
        if isinstance(python_object, float):
            # Okay, this is a weird one. The decimal module will crash if it is passed a float
            # with less than two decimal numbers, like float(0.5) which has only one. The decimal
            # module is used when using the Utils.TypeSerializer accessible via the serializer property.
            # Yet, the module has no issues with number with more than 20 decimals, and we want to keep
            # this infos, so we will not round the object. Instead, with the "%.f" % python_object we will
            # get the number of decimal numbers on the float (returned in the form of a string, for real,
            # and if this number is under two, we will turn the float into a float with two decimal numbers by
            # using "%.2f" % python_object, which will then be able to be passed to the Decimal modules without errors.
            # PS : Obviously, instead of doing this, a number like 0.5 cannot be converted to an int ;)
            if ("%.f" % python_object) < "2":
                python_object = "%.2f" % python_object

            return Decimal(python_object)
        elif isinstance(python_object, list):
            for i, item in enumerate(python_object):
                python_object[i] = Utils.float_serializer(python_object=item)
            return python_object
        elif isinstance(python_object, dict):
            for key, value in python_object.items():
                python_object[key] = Utils.float_serializer(python_object=value)
            return python_object
        else:
            return python_object

    def decimal_deserializer(self, python_object):
        from decimal import Decimal
        if isinstance(python_object, Decimal):
            if ("%.f" % python_object) > "0":
                python_object = float(python_object)
            else:
                python_object = int(python_object)
            return python_object
        elif isinstance(python_object, list):
            for i, item in enumerate(python_object):
                python_object[i] = Utils.decimal_deserializer(python_object=item)
            return python_object
        elif isinstance(python_object, dict):
            for key, value in python_object.items():
                python_object[key] = Utils.decimal_deserializer(python_object=value)
            return python_object
        else:
            return python_object

    @staticmethod
    def python_to_dynamodb(python_object: Any):
        """
            None                                    {'NULL': True}
            True/False                              {'BOOL': True/False}
            int/Decimal                             {'N': str(value)}
            string                                  {'S': string}
            Binary/bytearray/bytes (py3 only)       {'B': bytes}
            set([int/Decimal])                      {'NS': [str(value)]}
            set([string])                           {'SS': [string])
            set([Binary/bytearray/bytes])           {'BS': [bytes]}
            list                                    {'L': list}
            dict                                    {'M': dict}
        :param python_object:
        :return:
        """

        object_type = type(python_object)
        if object_type in [int, float]:
            return {Utils.TYPE_NUMBER: Utils._python_to_decimal(python_number=python_object)}
        elif object_type == list:
            for i, item in enumerate(python_object):
                python_object[i] = Utils.python_to_dynamodb(python_object=item)
            return {Utils.TYPE_LIST: python_object}
        elif object_type == dict:
            for key, item in python_object.items():
                python_object[key] = Utils.python_to_dynamodb(python_object=item)
            return {Utils.TYPE_MAP: python_object}
        elif object_type == bool:
            return {Utils.TYPE_BOOLEAN: python_object}
        elif object_type == str:
            return {Utils.TYPE_STRING: python_object}
        elif object_type == type(None):
            return {Utils.TYPE_NULL: True}
        elif object_type == bytes:
            return {Utils.TYPE_BINARY: python_object}
        else:
            return python_object

    @staticmethod
    def dynamodb_to_python(dynamodb_object: Any):
        if isinstance(dynamodb_object, Decimal):
            return Utils._decimal_to_python(decimal_number=dynamodb_object)
        elif isinstance(dynamodb_object, list):
            for i, item in enumerate(dynamodb_object):
                dynamodb_object[i] = Utils.dynamodb_to_python(dynamodb_object=item)
            return dynamodb_object
        elif isinstance(dynamodb_object, dict):
            if len(dynamodb_object) == 1:
                # If the length of the Dict is only one, it might be a DynamoDB object, with its key
                # as its variable type. For example : {'N': '1'}  And yes, this also apply to lists and maps.

                first_key = list(dynamodb_object.keys())[0]
                first_item = dynamodb_object[first_key]

                # First do we thing, is check if the value is a Decimal value (which happens often).
                if isinstance(first_item, Decimal):
                    return Utils._decimal_to_python(decimal_number=first_item)

                # Then the order of the elif statement is based on what we personally use the most at Inoft.
                # For example, we always use the numbers, string, list and dictionaries (maps) but always
                # never binary data or sets. In the default library, the list and dict were at the end of the loop.
                elif first_key == Utils.TYPE_NUMBER:
                    return Utils._dynamodb_number_to_python(number_string=first_item)
                elif first_key == Utils.TYPE_STRING:
                    return first_item
                elif first_key in Utils.ALL_TYPES_WHERE_VALUE_DO_NOT_NEED_MODIFICATIONS:
                    return first_item
                elif first_key == Utils.TYPE_MAP:
                    return dict([(key, Utils.dynamodb_to_python(element)) for key, element in first_item.items()])
                elif first_key == Utils.TYPE_LIST:
                    return [Utils.dynamodb_to_python(element) for element in first_item]
                elif first_key == Utils.TYPE_NULL:
                    return None
                elif first_key == Utils.TYPE_BINARY:
                    return Utils._dynamodb_binary_to_python(binary_data=first_item)
                elif first_key == Utils.TYPE_NUMBER_SET:
                    return set(map(Utils.DECIMAL_DYNAMODB_CONTEXT.create_decimal, first_item))
                elif first_key == Utils.TYPE_STRING_SET:
                    return set(first_item)
                elif first_key == Utils.TYPE_BINARY_SET:
                    from boto3.dynamodb.types import Binary
                    return set(map(Utils._dynamodb_binary_to_python, first_item))

            # If the dict was a classic dict, with its first key not in the keys used by DynamoDB
            keys_to_pop: List[str] = list()
            for key, item in dynamodb_object.items():
                item_value = Utils.dynamodb_to_python(dynamodb_object=item)
                if item_value is not None:
                    dynamodb_object[key] = item_value
                else:
                    keys_to_pop.append(key)

            for key in keys_to_pop:
                dynamodb_object.pop(key)

            return dynamodb_object
        else:
            return dynamodb_object

    @staticmethod
    def dynamodb_to_python_higher_level(dynamodb_object: Any):
        if isinstance(dynamodb_object, Decimal):
            return Utils._decimal_to_python(decimal_number=dynamodb_object)
        elif isinstance(dynamodb_object, list):
            for i, item in enumerate(dynamodb_object):
                dynamodb_object[i] = Utils.dynamodb_to_python_higher_level(dynamodb_object=item)
            return dynamodb_object
        elif isinstance(dynamodb_object, dict):
            # If the dict was a classic dict, with its first key not in the keys used by DynamoDB
            for key, item in dynamodb_object.items():
                dynamodb_object[key] = Utils.dynamodb_to_python_higher_level(dynamodb_object=item)
            return dynamodb_object
        return dynamodb_object

    @staticmethod
    def _decimal_to_python(decimal_number: Decimal) -> float or int:
        decimal_float = decimal_number.__float__()
        return decimal_float if decimal_float.is_integer() is not True else int(decimal_float)

    @staticmethod
    def _python_to_decimal(python_number: int or float) -> Decimal:
        return Utils.DECIMAL_DYNAMODB_CONTEXT.create_decimal(python_number)

    @staticmethod
    def _dynamodb_number_to_python(number_string: str):
        float_number = float(number_string)
        if float_number.is_integer():
            return int(float_number)
        else:
            return float_number

    @staticmethod
    def _dynamodb_binary_to_python(binary_data):
        from boto3.dynamodb.types import Binary
        return Binary(value=binary_data)

    @staticmethod
    def python_type_to_dynamodb_type(python_type):
        """
        {'NULL': True}                          None
        {'BOOL': True/False}                    True/False
        {'N': str(value)}                       Decimal(str(value))
        {'S': string}                           string
        {'B': bytes}                            Binary(bytes)
        {'NS': [str(value)]}                    set([Decimal(str(value))])
        {'SS': [string]}                        set([string])
        {'BS': [bytes]}                         set([bytes])
        {'L': list}                             list
        {'M': dict}                             dict
        """
        if python_type == type(None):
            return "NULL"
        elif python_type == bool:
            return "BOOL"
        elif python_type in [Decimal, int, float]:
            return "N"
        elif python_type == str:
            return "S"
        elif python_type == bytes:
            return "B"
        elif python_type == list:
            return "L"
        elif python_type == dict:
            return "M"
