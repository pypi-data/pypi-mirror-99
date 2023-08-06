# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.ICleanable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for cleanable components
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICleanable:
    """
    Interface for components that should clean their state.
    Cleaning state most often is used during testing.
    But there may be situations when it can be done in production.
    """
    def clear(self, correlation_id):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        raise NotImplementedError('Method from interface definition')
