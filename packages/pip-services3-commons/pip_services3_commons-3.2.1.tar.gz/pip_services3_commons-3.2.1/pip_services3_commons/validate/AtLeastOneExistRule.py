# -*- coding: utf-8 -*-
"""
    pip_services3_commons.validate.AtLeastOneExistRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    At least one exist rule implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IValidationRule import IValidationRule
from .ValidationResultType import ValidationResultType
from .ValidationResult import ValidationResult
from ..reflect.ObjectReader import ObjectReader

class AtLeastOneExistRule(IValidationRule):
    """
    Validation rule that check that at least one of the object properties is not None.

    Example:

    .. code-block:: python

        schema = Schema().with_rule(AtLeastOneExistsRule("field1", "field2"))
        schema.validate({ field1: 1, field2: "A" })     # Result: no errors
        schema.validate({ field1: 1 })                  # Result: no errors
        schema.validate({ })                            # Result: at least one of properties field1, field2 must exist
    """
    _properties = None

    def __init__(self, *properties):
        """
        Creates a new validation rule and sets its values

        :param properties: a list of property names where at least one property must exist
        """
        self._properties = properties
    
    def validate(self, path, schema, value, results):
        """
        Validates a given value against this rule.

        :param path: a dot notation path to the value.

        :param schema: a schema this rule is called from

        :param value: a value to be validated.

        :param results: a list with validation results to add new results.
        """
        name = path if not (path is None) else "value"
        found = []

        for prop in self._properties:
            property_value = ObjectReader.get_property(value, prop)
            if not (property_value is None):
                found.append(prop)

        if len(found) == 0:
            results.append(
                ValidationResult(
                    path,
                    ValidationResultType.Error,
                    "VALUE_NULL",
                    name + " must have at least one property from " + str(self._properties),
                    self._properties,
                    None
                )
            )
