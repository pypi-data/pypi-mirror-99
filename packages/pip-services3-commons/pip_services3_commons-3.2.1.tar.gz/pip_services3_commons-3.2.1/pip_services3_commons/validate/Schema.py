# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.Schema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation schema for complex objects.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ValidationException import ValidationException
from .ValidationResult import ValidationResult
from .ValidationResultType import ValidationResultType
from ..convert.TypeConverter import TypeConverter
from ..reflect.ObjectReader import ObjectReader
from ..reflect.TypeMatcher import TypeMatcher


class Schema(object):
    """
    Basic schema that validates values against a set of validation rules.

    This schema is used as a basis for specific schemas to validate
    objects, project properties, arrays and maps.
    """
    required = None
    rules = None

    def __init__(self, required=False, rules=None):
        """
        Creates a new instance of validation schema and sets its values.

        :param required: (optional) true to always require non-null values.

        :param rules: (optional) a list with validation rules.
        """
        self.required = required
        self.rules = rules if not (rules is None) else []

    def is_required(self):
        """
        Gets a flag that always requires non-null values.
        For null values it raises a validation error.

        :return: true to always require non-null values and false to allow null values.
        """
        return self.required

    def set_required(self, value):
        """
        Sets a flag that always requires non-null values.

        :param value: true to always require non-null values and false to allow null values.
        """
        self.required = value

    def get_rules(self):
        """
        Gets validation rules to check values against.

        :return: a list with validation rules.
        """
        return self.rules

    def set_results(self, value):
        """
        Sets validation rules to check values against.

        :param value: a list with validation rules.
        """
        self.rules = value

    def make_required(self):
        """
        Makes validated values always required (non-null).
        For null values the schema will raise errors.

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :return: this validation schema
        """
        self.required = True
        return self

    def make_optional(self):
        """
        Makes validated values optional.
        Validation for null values will be skipped.

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :return: this validation schema
        """
        self.required = False
        return self

    def with_rule(self, rule):
        """
        Adds validation rule to this schema.

        This method returns reference to this exception to implement Builder pattern
        to chain additional calls.

        :param rule: a validation rule to be added.

        :return: this validation schema.
        """
        self.rules = self.rules if not (self.rules is None) else []
        self.rules.append(rule)
        return self

    def _perform_validation(self, path, value, results):
        """
        Validates a given value against the schema and configured validation rules.

        :param path: a dot notation path to the value.

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if not (path is None) else "value"

        if value is None:
            # Check for required values
            if self.required:
                results.append(
                    ValidationResult(
                        path,
                        ValidationResultType.Error,
                        "VALUE_IS_NULL",
                        name + " cannot be null",
                        "NOT NULL",
                        None
                    )
                )
        else:
            value = ObjectReader.get_value(value)

            # Check validation rules
            if not (self.rules is None):
                for rule in self.rules:
                    rule.validate(path, self, value, results)

    def _type_to_string(self, typ):
        if typ is None:
            return "unknown"
        if isinstance(typ, int):
            return TypeConverter.to_string(typ)
        return TypeConverter.to_string(typ)

    def _perform_type_validation(self, path, typ, value, results):
        """
        Validates a given value to match specified type.
        The type can be defined as a Schema, type, a type name or :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>`.
        When type is a Schema, it executes validation recursively against that Schema.

        :param path: a dot notation path to the value.

        :param typ: a type to match the value type

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        # If type it not defined then skip
        if typ is None:
            return

        # Perform validation against schema
        if isinstance(typ, Schema):
            schema = typ
            schema._perform_validation(path, value, results)
            return

        # If value is null then skip
        value = ObjectReader.get_value(value)
        if value is None:
            return

        name = path or "value"
        value_type = TypeConverter.to_type_code(value)

        # Match types
        if TypeMatcher.match_type(typ, value_type, value):
            return

        # Generate type mismatch error
        results.append(
            ValidationResult(
                path,
                ValidationResultType.Error,
                "TYPE_MISMATCH",
                name + " type must be " +
                self._type_to_string(typ) + " but found " +
                self._type_to_string(value_type),
                typ,
                value_type
            )
        )

    def validate(self, value):
        """
        Validates the given value and results validation results.

        :param value: a value to be validated.

        :return: a list with validation results.
        """
        results = []
        self._perform_validation("", value, results)
        return results

    def validate_and_return_exception(self, correlation_id, value, strict=False):
        """
        Validates the given value and returns a :class:`ValidationException <pip_services3_commons.validate.ValidationException.ValidationException>` if errors were found.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param value: a value to be validated.
        :param strict: true to treat warnings as errors.
        """
        results = self.validate(value)
        return ValidationException.from_results(correlation_id, results, strict)

    def validate_and_throw_exception(self, correlation_id, value, strict=False):
        """
        Validates the given value and throws a :class:`ValidationException <pip_services3_commons.validate.ValidationException.ValidationException>` if errors were found.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param value: a value to be validated.

        :param strict: true to treat warnings as errors.
        """
        results = self.validate(value)
        ValidationException.throw_exception_if_needed(
            correlation_id, results, strict)
