# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.Parameters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Parameters component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from ..data.AnyValueMap import AnyValueMap
from ..convert.JsonConverter import JsonConverter
from ..reflect.RecursiveObjectReader import RecursiveObjectReader
from ..reflect.RecursiveObjectWriter import RecursiveObjectWriter
from ..reflect.ObjectWriter import ObjectWriter

class Parameters(AnyValueMap):
    """
    Contains map with execution parameters.

    In general, this map may contain non-serializable values.
    And in contrast with other maps, its getters and setters
    support dot notation and able to access properties in the entire object graph.

    This class is often use to pass execution and notification
    arguments, and parameterize classes before execution.
    """
    def __init__(self, map = None):
        """
        Creates a new instance of the map and assigns its value.

        :param map:(optional) values to initialize this map.
        """
        super(Parameters, self).__init__(map)

    def get(self, key):
        """
        Gets a map element specified by its key.

        The key can be defined using dot notation
        and allows to recursively access elements of elements.

        :param key: a key of the element to get.

        :return: the value of the map element.
        """
        if key is None or key == '':
            return None
        elif key.find('.') > 0:
            return RecursiveObjectReader.get_property(self, key)
        else:
            return super(Parameters, self).get(key)

    def put(self, key, value):
        """
        Puts a new value into map element specified by its key.

        The key can be defined using dot notation
        and allows to recursively access elements of elements.

        :param key: a key of the element to put.

        :param value: a new value for map element.
        """
        if key is None or key == '':
            return None
        elif key.find('.') > 0:
            RecursiveObjectWriter.set_property(self, key, value)
            return value
        else:
            self[key] = value
            return value

    def get_as_nullable_parameters(self, key):
        """
        Converts map element into an Parameters or returns null if conversion is not possible.

        :param key: a key of element to get.

        :return: Parameters value of the element or null if conversion is not supported.
        """
        value = self.get_as_nullable_map(key)
        return Parameters(value) if not (value is None) else None

    def get_as_parameters(self, key):
        """
        Converts map element into an Parameters or returns empty Parameters if conversion is not possible.

        :param key: a key of element to get.

        :return: Parameters value of the element or empty Parameters if conversion is not supported.
        """
        value = self.get_as_map(key)
        return Parameters(value)

    def get_as_parameters_with_default(self, key, default_value):
        """
        Converts map element into an Parameters or returns default value if conversion is not possible.

        :param key: a key of element to get.

        :param default_value: the default value

        :return: Parameters value of the element or default value if conversion is not supported.
        """
        result = self.get_as_nullable_parameters(key)
        return result if not (result is None) else default_value

    def contains_key(self, key):
        """
        Checks if this map contains an element with specified key.

        The key can be defined using dot notation
        and allows to recursively access elements of elements.

        :param key: a key to be checked

        :return: true if this map contains the key or false otherwise.
        """
        return RecursiveObjectReader.has_property(self, key)

    def override(self, parameters, recursive = False):
        """
        Overrides parameters with new values from specified Parameters and returns a new Parameters object.

        :param parameters: Parameters with parameters to override the current values.

        :param recursive: (optional) true to perform deep copy, and false for shallow copy. Default: false

        :return: a new Parameters object.
        """
        result = Parameters()

        if recursive:
            RecursiveObjectWriter.copy_properties(result, self)
            RecursiveObjectWriter.copy_properties(result, parameters)
        else:
            ObjectWriter.set_properties(result, self)
            ObjectWriter.set_properties(result, parameters)

        return result

    def set_defaults(self, default_values, recursive = False):
        """
        Set default values from specified Parameters and returns a new Parameters object.

        :param default_values: Parameters with default parameter values.

        :param recursive: (optional) true to perform deep copy, and false for shallow copy. Default: false

        :return: a new Parameters object.
        """
        result = Parameters()

        if recursive:
            RecursiveObjectWriter.copy_properties(result, default_values)
            RecursiveObjectWriter.copy_properties(result, self)
        else:
            ObjectWriter.set_properties(result, default_values)
            ObjectWriter.set_properties(result, self)

        return result

    def assign_to(self, value):
        """
        Assigns (copies over) properties from the specified value to this map.

        :param value: value whose properties shall be copied over.
        """
        if value is None or len(self) == 0:
            return

        RecursiveObjectWriter.copy_properties(value, self)
        
    def pick(self, *props):
        """
        Picks select parameters from this Parameters and returns them as a new Parameters object.

        :param props: keys to be picked and copied over to new Parameters.

        :return: a new Parameters object.
        """
        result = Parameters()
        for prop in props:
            if self.contains_key(prop):
                result.put(prop, self.get(prop))
        return result

    def omit(self, *props):
        """
        Omits selected parameters from this Parameters and returns the rest as a new Parameters object.

        :param props: keys to be omitted from copying over to new Parameters.

        :return: a new Parameters object.
        """
        result = Parameters(self)
        for prop in props:
            del result[prop]
        return result

    def to_json(self):
        """
        Converts this map to JSON object.

        :return: a JSON representation of this map.
        """
        return JsonConverter.to_json(self)

    @staticmethod
    def from_value(value):
        """
        Creates a new Parameters object filled with key-value pairs from specified object.

        :param value: an object with key-value pairs used to initialize a new Parameters.

        :return: a new Parameters object.
        """
        map = value if isinstance(value, dict) else RecursiveObjectReader.get_properties(value)
        return Parameters(map)

    @staticmethod
    def from_tuples(*tuples):
        """
        Creates a new Parameters object filled with provided key-value pairs called tuples.
        Tuples parameters contain a sequence of key1, value1, key2, value2, ... pairs.

        :param tuples: the tuples to fill a new Parameters object.

        :return: a new Parameters object.
        """
        map = AnyValueMap.from_tuples_array(tuples)
        return Parameters(map)

    @staticmethod
    def merge_params(*parameters):
        """
        Merges two or more Parameters into one. The following Parameters override previously defined parameters.

        :param parameters: a list of Parameters objects to be merged.

        :return: a new Parameters object.
        """
        map = AnyValueMap.from_maps(parameters)
        return Parameters(map)

    @staticmethod
    def from_json(json):
        """
        Creates new Parameters from JSON object.

        :param json: a JSON string containing parameters.

        :return: a new Parameters object.
        """
        map = JsonConverter.to_nullable_map(json)
        return Parameters(map)

    @staticmethod
    def from_config(config):
        """
        Creates new Parameters from ConfigMap object.

        :param config: a ConfigParams that contain parameters.

        :return: a new Parameters object.
        """
        result = Parameters()
        
        if config is None or len(config) == 0:
            return result
        
        for (key, value) in config.items():
            result.put(key, value)
        
        return result
