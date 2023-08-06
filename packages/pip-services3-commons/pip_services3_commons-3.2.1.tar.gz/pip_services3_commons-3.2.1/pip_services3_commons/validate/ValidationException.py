# -*- coding: utf-8 -*-
"""
    pip_services_common.validate.ValidationException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Validation exception type
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ValidationResultType import ValidationResultType
from ..errors.BadRequestException import BadRequestException


class ValidationException(BadRequestException):
    """
    Errors in schema validation.

    Validation errors are usually generated based in :class:`ValidationResult <pip_services3_commons.validate.ValidationResult.ValidationResult>`.
    If using strict mode, warnings will also raise validation exceptions.
    """

    def __init__(self, correlation_id, message, results):
        """
        Creates a new instance of validation exception and assigns its values.

        :param correlation_id: (optional) a unique transaction id to trace execution through call chain.

        :param results: (optional) a list of validation results

        :param message: (optional) a human-readable description of the error.
        """
        super(BadRequestException, self).__init__(correlation_id, 'INVALID_DATA',
                                                  ValidationException.compose_message(results) or message)

    @staticmethod
    def compose_message(results):
        """
        Composes human readable error message based on validation results.

        :param results: a list of validation results.

        :return: a composed error message.
        """
        message = ''
        message += 'Validation failed'

        if not (results is None) and len(results) > 0:
            first = True
            for result in results:
                if result.get_type() != ValidationResultType.Information:
                    if not first:
                        message += ': '
                    else:
                        message += ', '
                    message += result.get_message()
                    first = False

        return message

    @staticmethod
    def from_results(correlation_id, results, strict):
        """
        Creates a new ValidationException based on errors in validation results.
        If validation results have no errors, than null is returned.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        :param results: list of validation results that may contain errors
        :param strict: true to treat warnings as errors.
        :return: a newly created ValidationException or null if no errors in found.
        """
        has_errors = False

        for i in range(len(results)):
            result = results[i]

            if result.get_type() == ValidationResultType.Error:
                has_errors = True

            if strict and result.get_type() == ValidationResultType.Warning:
                has_errors = True

        return ValidationException(correlation_id, None, results) if has_errors else None

    @staticmethod
    def throw_exception_if_needed(correlation_id, results, strict):
        """
        Throws ValidationException based on errors in validation results.
        If validation results have no errors, than no exception is thrown.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param results: list of validation results that may contain errors

        :param strict: true to treat warnings as errors.
        """
        has_errors = False
        for result in results:
            if result.get_type() == ValidationResultType.Error:
                has_errors = True
            if strict and result.get_type() == ValidationResultType.Warning:
                has_errors = True

        if has_errors:
            raise ValidationException.from_results(correlation_id, results, strict)
