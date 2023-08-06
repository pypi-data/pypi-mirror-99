# -*- coding: utf-8 -*-
"""
    pip_services3_commons.reflect.TypeMatcher
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type matcher implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.convert import TypeCode, TypeConverter, DateTimeConverter


class TypeMatcher:
    """
    Helper class matches value types for equality.

    This class has symmetric implementation across all languages supported
    by Pip.Services toolkit and used to support dynamic data processing.
    """

    @staticmethod
    def match_value(expected_type, actual_value):
        """
        Matches expected type to a type of a value.
        The expected type can be specified by a type, type name or :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>`.

        :param expected_type: an expected type to match.

        :param actual_value: a value to match its type to the expected one.

        :return: True if types are matching and False if they don't.
        """
        if expected_type is None:
            return True
        if actual_value is None:
            raise Exception("Actual value cannot be null")

        return TypeMatcher.match_type(expected_type, TypeConverter.to_type_code(actual_value), actual_value)

    @staticmethod
    def match_type(expected_type, actual_type, actual_value=None):
        """
        Matches expected type to an actual type.
        The types can be specified as types, type names or :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>`.

        :param expected_type: an expected type to match.

        :param actual_type: an actual type to match.

        :param actual_value: an optional value to match its type to the expected one.

        :return: True if types are matching and False if they don't.
        """
        if expected_type is None:
            return True
        if actual_type is None:
            raise Exception("Actual type cannot be null")

        if isinstance(expected_type, type):
            return issubclass(type(actual_value), expected_type)

        if isinstance(expected_type, int):
            if expected_type == actual_type:
                return True

            # Special provisions for dynamic data
            if expected_type == TypeCode.Integer and (
                    actual_type == TypeCode.Long or actual_type == TypeCode.Float or actual_type == TypeCode.Double):
                return True

            if expected_type == TypeCode.Long and (
                    actual_type == TypeCode.Integer or actual_type == TypeCode.Float or actual_type == TypeCode.Double):
                return True

            if expected_type == TypeCode.Float and (
                    actual_type == TypeCode.Integer or actual_type == TypeCode.Long or actual_type == TypeCode.Double):
                return True

            if expected_type == TypeCode.Double and (
                    actual_type == TypeCode.Integer or actual_type == TypeCode.Long or actual_type == TypeCode.Float):
                return True

            if expected_type == TypeCode.DateTime and (
                    actual_type == TypeCode.String
                    and DateTimeConverter.to_nullable_datetime(actual_value) is not None):
                return True

        if isinstance(expected_type, str):
            return TypeMatcher.match_type_by_name(expected_type, actual_type, actual_value)

        return False

    @staticmethod
    def match_value_type_by_name(expected_type, actual_value):
        """
        Matches expected type to a type of a value.

        :param expected_type: an expected type name to match.

        :param actual_value: a value to match its type to the expected one.

        :return: True if types are matching and False if they don't.
        """
        if expected_type is None:
            return True
        if actual_value is None:
            raise Exception("Actual value cannot be null")

        return TypeMatcher.match_type_by_name(expected_type, TypeConverter.to_type_code(actual_value), actual_value)

    @staticmethod
    def match_type_by_name(expected_type, actual_type, actual_value=None):
        """
        Matches expected type to an actual type.

        :param expected_type: an expected type name to match.

        :param actual_type: an actual type to match defined by type code.

        :param actual_value: an optional value to match its type to the expected one.

        :return: true if types are matching and false if they don't.
        """
        if expected_type is None:
            return True
        if actual_type is None:
            raise Exception("Actual type cannot be null")

        expected_type = expected_type.lower()

        if type(actual_value).__name__.lower() == expected_type:
            return True

        if expected_type == "object":
            return True
        elif expected_type == "int" or expected_type == "integer":
            # Special provisions for dynamic data
            return actual_type == TypeCode.Integer or actual_type == TypeCode.Long
        elif expected_type == "long":
            # Special provisions for dynamic data
            return actual_type == TypeCode.Long or actual_type == TypeCode.Integer
        elif expected_type == "float" or expected_type == "double":
            # Special provisions for dynamic data
            return actual_type == TypeCode.Float \
                   or actual_type == TypeCode.Double \
                   or actual_type == TypeCode.Integer \
                   or actual_type == TypeCode.Long
        elif expected_type == "string":
            return actual_type == TypeCode.String
        elif expected_type == "bool" or expected_type == "boolean":
            return actual_type == TypeCode.Boolean
        elif expected_type == "date" or expected_type == "datetime":
            # Special provisions fro dynamic data
            return actual_type == TypeCode.DateTime \
                   or (actual_type == TypeCode.String
                       and DateTimeConverter.to_nullable_datetime(actual_value) is not None)
        elif expected_type == "timespan" or expected_type == "duration":
            return actual_type == TypeCode.Integer \
                   or actual_type == TypeCode.Long \
                   or actual_type == TypeCode.Float \
                   or actual_type == TypeCode.Double
        elif expected_type == "enum":
            return actual_type == TypeCode.Integer or actual_type == TypeCode.String

        elif expected_type == "map" or expected_type == "dict" or expected_type == "dictionary":
            return actual_type == TypeCode.Map
        elif expected_type == "array" or expected_type == "list":
            return actual_type == TypeCode.Array
        elif expected_type.endswith("[]"):
            # Todo: Check subtype
            return actual_type == TypeCode.Array
        else:
            return False
