# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.JsonConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Json conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import json
from datetime import datetime

from .MapConverter import MapConverter
from .TypeConverter import TypeConverter


class JsonConverter():
    """
    Converts arbitrary values from and to JSON (JavaScript Object Notation) strings.

    Example:

    .. code-block:: python
    
        value1 = JsonConverter.from_json("{\"key\":123}") // Result: { key: 123 }
        value2 = JsonConverter.to_map({ key: 123}) // Result: "{\"key\":123}"
    """

    @staticmethod
    def from_json(typ, value):
        """
        Converts JSON string into a value.

        :param typ: the TypeCode for the data type into which 'value' is to be converted.

        :param value: the JSON string to convert.

        :return: converted object value or null when value is None.
        """
        if value is None:
            return None

        value = json.loads(value)
        return TypeConverter.to_type(typ, value)

    @staticmethod
    def to_json(value):
        """
        Converts value into JSON string.

        :param value: the value to convert.

        :return: JSON string or null when value is None.
        """
        if value is None:
            return None

        if isinstance(value, datetime):
            str_time = value.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            return (str_time[:-8] + str_time[-5:]).split('+')[0] + 'Z'  # Remove microseconds

        return json.dumps(value)

    @staticmethod
    def to_nullable_map(value):
        """
        Converts JSON string into map object or returns null when conversion is not possible.

        :param value: the JSON string to convert.

        :return: Map object value or null when conversion is not supported.
        """
        if value is None:
            return None

        # Parse JSON
        try:
            value = json.loads(value)
            return MapConverter.to_nullable_map(value)
        except:
            return None

    @staticmethod
    def to_map(value):
        """
        Converts JSON string into map object or returns empty map when conversion is not possible.

        :param value: the JSON string to convert.

        :return: Map object value or empty object when conversion is not supported.
        """
        result = JsonConverter.to_nullable_map(value)
        return result if not (result is None) else {}

    @staticmethod
    def to_map_with_default(value, default_value):
        """
        Converts JSON string into map object or returns default value when conversion is not possible.

        :param value: the JSON string to convert.

        :param default_value: the default value.

        :return: Map object value or default when conversion is not supported.
        """
        result = JsonConverter.to_nullable_map(value)
        return result if not (result is None) else default_value
