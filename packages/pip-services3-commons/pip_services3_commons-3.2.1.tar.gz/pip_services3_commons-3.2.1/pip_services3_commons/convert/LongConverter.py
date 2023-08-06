# -*- coding: utf-8 -*-
"""
    pip_services3_commons.convert.LongConverter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Long conversion utilities
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import inspect
from datetime import datetime


class LongConverter():

    @staticmethod
    def to_nullable_long(value):
        if value is None:
            return None
        if type(value) == int or isinstance(value, float):
            return int(value)
        if isinstance(value, datetime) or inspect.isclass(value) and issubclass(value, datetime):
            return int(value.timestamp() * 1000)
        if isinstance(value, bool):
            return 1 if value else 0

        try:
            result = float(value)
        except ValueError:
            return None

        return None if result is None else int(result)

    @staticmethod
    def to_long(value):
        return LongConverter.to_long_with_default(value, 0)

    @staticmethod
    def to_long_with_default(value, default_value):
        result = LongConverter.to_nullable_long(value)
        return result if not (result is None) else default_value
