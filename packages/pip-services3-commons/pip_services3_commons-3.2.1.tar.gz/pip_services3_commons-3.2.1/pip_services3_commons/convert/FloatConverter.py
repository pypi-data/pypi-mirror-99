# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.FloatConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Float conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services3_commons.convert.DoubleConverter import DoubleConverter


class FloatConverter():
    """
    Converts arbitrary values into float using extended conversion rules:
    - Strings are converted to float values
    - DateTime: total number of milliseconds since unix epoсh
    - Boolean: 1 for true and 0 for false

    Example:
    .. code-block:: python
        value1 = FloatConverter.to_nullable_float("ABC")     # Result: None
        value2 = FloatConverter.to_nullable_float("123.456") # Result: 123.456
        value3 = FloatConverter.to_nullable_float(true)      # Result: 1
        value4 = FloatConverter.to_nullable_float(datetime.datetime.now()) # Result: current milliseconds
    """

    @staticmethod
    def to_nullable_float(value):
        """
        Converts value into float or returns null when conversion is not possible.

        :param value: the value to convert.

        :return: float value or null when conversion is not supported.
        """
        # Shortcuts
        return DoubleConverter.to_nullable_double(value)

    @staticmethod
    def to_float(value):
        """
        Converts value into float or returns 0 when conversion is not possible.

        :param value: the value to convert.

        :return: float value or 0 when conversion is not supported.
        """
        return DoubleConverter.to_double(value)

    @staticmethod
    def to_float_with_default(value, default_value):
        """
        Converts value into float or returns default when conversion is not possible.

        :param value: the value to convert.

        :param default_value: the default value.

        :return: float value or default value when conversion is not supported.
        """
        return DoubleConverter.to_double_with_default(value, default_value)
