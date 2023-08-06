# -*- coding: utf-8 -*-
"""
    pip_services3_commons.reflect.MethodReflector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Method reflector implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class MethodReflector:
    """
    Helper class to perform method introspection and dynamic invocation.
    This class has symmetric implementation across all languages supported
    by Pip.Services toolkit and used to support dynamic data processing.

    Because all languages have different casing and case sensitivity rules,
    this MethodReflector treats all method names as case insensitive.

    Example:

    .. code-block:: python
    
        myObj = new MyObject()

        methods = MethodReflector.get_method_names()
        MethodReflector.has_method(myObj, "myMethod")
        MethodReflector.invoke_method(myObj, "myMethod", 123)
    """
    @staticmethod
    def _is_method(method, name):
        if method is None:
            return False
        if not callable(method):
            return False

        if name.startswith("_"):
            return False

        return True 


    @staticmethod
    def has_method(obj, name):
        """
        Checks if object has a method with specified name.

        :param obj: an object to introspect.

        :param name: a name of the method to check.

        :return: true if the object has the method and false if it doesn't.
        """
        if obj is None:
            raise Exception("Object cannot be null")
        if name is None:
            raise Exception("Method name cannot be null")

        name = name.lower()

        for method_name in dir(obj): 
            if method_name.lower() != name:
                continue

            method = getattr(obj, method_name)

            if MethodReflector._is_method(method, method_name):
                return True
        
        return False


    @staticmethod
    def invoke_method(obj, name, *args):
        """
        Invokes an object method by its name with specified parameters.

        :param obj: an object to invoke.

        :param name: a name of the method to invoke.

        :param args: a list of method arguments.

        :return: the result of the method invocation or null if method returns void.
        """
        if obj is None:
            raise Exception("Object cannot be null")
        if name is None:
            raise Exception("Method name cannot be null")
        
        name = name.lower()
        
        try:
            for method_name in dir(obj): 
                if method_name.lower() != name:
                    continue

                method = getattr(obj, method_name)

                if MethodReflector._is_method(method, method_name):
                    return method(*args)
        except:
            pass
        
        return None


    @staticmethod
    def get_method_names(obj):
        """
        Gets names of all methods implemented in specified object.

        :param obj: an object to introspect.

        :return: a list with method names.
        """
        method_names = []
        
        for method_name in dir(obj):

            method = getattr(obj, method_name)

            if MethodReflector._is_method(method, method_name):
                method_names.append(method_name)

        return method_names
