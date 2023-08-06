﻿'''_6520.py

ScriptedPropertyNameAttribute
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_SCRIPTED_PROPERTY_NAME_ATTRIBUTE = python_net_import('SMT.MastaAPIUtility', 'ScriptedPropertyNameAttribute')


__docformat__ = 'restructuredtext en'
__all__ = ('ScriptedPropertyNameAttribute',)


class ScriptedPropertyNameAttribute:
    '''ScriptedPropertyNameAttribute

    This is a mastapy class.
    '''

    TYPE = _SCRIPTED_PROPERTY_NAME_ATTRIBUTE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ScriptedPropertyNameAttribute.TYPE'):
        self.wrapped = instance_to_wrap

    @property
    def property_name(self) -> 'str':
        '''str: 'PropertyName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PropertyName
