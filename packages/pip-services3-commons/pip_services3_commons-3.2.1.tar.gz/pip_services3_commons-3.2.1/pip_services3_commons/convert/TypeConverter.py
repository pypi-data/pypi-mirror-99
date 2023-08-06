# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.TypeConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime

from .ArrayConverter import ArrayConverter
from .DateTimeConverter import DateTimeConverter
from .FloatConverter import FloatConverter
from .IntegerConverter import IntegerConverter
from .LongConverter import LongConverter
from .MapConverter import MapConverter
from .StringConverter import StringConverter
from .TypeCode import TypeCode


class TypeConverter:
    """
    Converts arbitrary values into objects specific by TypeCodes.
    For each TypeCode this class calls corresponding converter which applies
    extended conversion rules to convert the values.

    Example:

    .. code-block:: python

        value1 = TypeConverter.to_type(TypeCode.Integer, "123.456") // Result: 123
        value2 = TypeConverter.to_type(TypeCode.DateTime, 123) // Result: Date(123)
        value3 = TypeConverter.to_type(TypeCode.Boolean, "F") // Result: false
    """

    @staticmethod
    def to_type_code(value):
        """
        Gets :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>` for specific value.

        :param value: value whose TypeCode is to be resolved.

        :return: the TypeCode that corresponds to the passed object's type.
        """
        if value is None:
            return TypeCode.Unknown

        if not isinstance(value, type):
            value = type(value)

        if value is list or issubclass(value, list):
            return TypeCode.Array
        elif value is tuple or issubclass(value, tuple):
            return TypeCode.Array
        elif value is set or issubclass(value, set):
            return TypeCode.Array
        elif value is bool or issubclass(value, bool):
            return TypeCode.Boolean
        elif value is int or issubclass(value, int):
            return TypeCode.Integer
        # elif value is long:
        #     return TypeCode.Long
        elif value is float or issubclass(value, float):
            return TypeCode.Float
        elif value is str or issubclass(value, str):
            return TypeCode.String
        # elif value is unicode:
        #     return TypeCode.String
        elif value is datetime or issubclass(value, datetime):
            return TypeCode.DateTime
        elif value is dict or issubclass(value, dict):
            return TypeCode.Map

        return TypeCode.Object

    @staticmethod
    def to_nullable_type(value_type, value):
        """
        Converts value into an object type specified by Type Code or returns null when conversion is not possible.

        :param value_type: the TypeCode for the data type into which 'value' is to be converted.

        :param value: the value to convert.

        :return: object value of type corresponding to TypeCode, or null when conversion is not supported.
        """
        value_type = TypeConverter.to_type_code(value_type) if isinstance(value_type, type) else value_type

        if value is None:
            return None

        # Convert to known types
        if value_type == TypeCode.String:
            return StringConverter.to_nullable_string(value)
        elif value_type == TypeCode.Integer:
            return IntegerConverter.to_nullable_integer(value)
        elif value_type == TypeCode.Long:
            return LongConverter.to_nullable_long(value)
        elif value_type == TypeCode.Float:
            return FloatConverter.to_nullable_float(value)
        elif value_type == TypeCode.Double:
            return FloatConverter.to_nullable_float(value)
        elif value_type == TypeCode.Duration:
            return LongConverter.to_nullable_long(value)
        elif value_type == TypeCode.DateTime:
            return DateTimeConverter.to_nullable_datetime(value)
        elif value_type == TypeCode.Array:
            return ArrayConverter.to_nullable_array(value)
        elif value_type == TypeCode.Map:
            return MapConverter.to_nullable_map(value)

        return value

    @staticmethod
    def to_type(value_type, value):
        """
        Converts value into an object type specified by Type Code or returns type default when conversion is not possible.

        :param value_type: the TypeCode for the data type into which 'value' is to be converted.

        :param value: the value to convert.

        :return: object value of type corresponding to TypeCode, or type default when conversion is not supported.
        """
        # Convert to the specified type
        result = TypeConverter.to_nullable_type(value_type, value)
        if result is not None:
            return result

        # Define and return default value based on type
        result_type = TypeConverter.to_type_code(value_type)
        if result_type == TypeCode.String:
            return ''
        elif result_type == TypeCode.Integer:
            return 0
        elif result_type == TypeCode.Long:
            return 0
        elif result_type == TypeCode.Float:
            return 0.0
        elif result_type == TypeCode.Double:
            return 0
        elif result_type == TypeCode.Boolean:
            return False
        elif result_type == TypeCode.DateTime:
            return datetime.now()
        elif result_type == TypeCode.Map:
            return {}
        elif result_type == TypeCode.Array:
            return []
        else:
            return None

    @staticmethod
    def to_type_with_default(value_type, value, default_value):
        """
        Converts value into an object type specified by Type Code or returns default value when conversion is not possible.

        :param value_type: the :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>` for the data type into which 'value' is to be converted.

        :param value: the value to convert.

        :param default_value: the default value to return if conversion is not possible (returns None).

        :return: object value of type corresponding to :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>`, or default value when conversion is not supported.
        """
        result = TypeConverter.to_nullable_type(value_type, value)
        return result if not (result is None) else default_value

    @staticmethod
    def to_string(typ):
        """
        Converts a :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>` into its string name.

        :param typ: the TypeCode to convert into a string.

        :return: the name of the TypeCode passed as a string value.
        """
        if typ is None:
            return "unknown"
        elif typ == TypeCode.Unknown:
            return "unknown"
        elif typ == TypeCode.String:
            return "string"
        elif typ == TypeCode.Integer:
            return "integer"
        elif typ == TypeCode.Long:
            return "long"
        elif typ == TypeCode.Float:
            return "float"
        elif typ == TypeCode.Double:
            return "double"
        elif typ == TypeCode.Duration:
            return "duration"
        elif typ == TypeCode.DateTime:
            return "datetime"
        elif typ == TypeCode.Object:
            return "object"
        elif typ == TypeCode.Enum:
            return "enum"
        elif typ == TypeCode.Array:
            return "array"
        elif typ == TypeCode.Map:
            return "map"
        else:
            return "unknown"
