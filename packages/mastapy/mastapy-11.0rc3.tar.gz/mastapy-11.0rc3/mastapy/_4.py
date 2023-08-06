﻿'''_4.py

UtilityMethods
'''


from typing import Callable, TypeVar

from mastapy import _0
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_UTILITY_METHODS = python_net_import('SMT.MastaAPI', 'UtilityMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('UtilityMethods',)


class UtilityMethods:
    '''UtilityMethods

    This is a mastapy class.
    '''

    TYPE = _UTILITY_METHODS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UtilityMethods.TYPE'):
        self.wrapped = instance_to_wrap

    T_is_read_only = TypeVar('T_is_read_only', bound='_0.APIBase')

    @staticmethod
    def is_read_only(entity: 'T_is_read_only', property_: 'Callable[[T_is_read_only], object]') -> 'bool':
        ''' 'IsReadOnly' is the original name of this method.

        Args:
            entity (T_is_read_only)
            property_ (Callable[[T_is_read_only], object])

        Returns:
            bool
        '''

        method_result = UtilityMethods.TYPE.IsReadOnly(entity.wrapped if entity else None, property_)
        return method_result

    T_is_invalidated = TypeVar('T_is_invalidated', bound='_0.APIBase')

    @staticmethod
    def is_invalidated(entity: 'T_is_invalidated', property_: 'Callable[[T_is_invalidated], object]') -> 'bool':
        ''' 'IsInvalidated' is the original name of this method.

        Args:
            entity (T_is_invalidated)
            property_ (Callable[[T_is_invalidated], object])

        Returns:
            bool
        '''

        method_result = UtilityMethods.TYPE.IsInvalidated(entity.wrapped if entity else None, property_)
        return method_result

    T_is_method_invalidated = TypeVar('T_is_method_invalidated', bound='_0.APIBase')

    @staticmethod
    def is_method_invalidated(entity: 'T_is_method_invalidated', method: 'Callable[[T_is_method_invalidated], Callable[..., None]]') -> 'bool':
        ''' 'IsMethodInvalidated' is the original name of this method.

        Args:
            entity (T_is_method_invalidated)
            method (Callable[[T_is_method_invalidated], Callable[..., None]])

        Returns:
            bool
        '''

        method_result = UtilityMethods.TYPE.IsMethodInvalidated(entity.wrapped if entity else None, method)
        return method_result

    T_is_method_read_only = TypeVar('T_is_method_read_only', bound='_0.APIBase')

    @staticmethod
    def is_method_read_only(entity: 'T_is_method_read_only', method: 'Callable[[T_is_method_read_only], Callable[..., None]]') -> 'bool':
        ''' 'IsMethodReadOnly' is the original name of this method.

        Args:
            entity (T_is_method_read_only)
            method (Callable[[T_is_method_read_only], Callable[..., None]])

        Returns:
            bool
        '''

        method_result = UtilityMethods.TYPE.IsMethodReadOnly(entity.wrapped if entity else None, method)
        return method_result

    @staticmethod
    def initialise_api_access(installation_directory: 'str'):
        ''' 'InitialiseApiAccess' is the original name of this method.

        Args:
            installation_directory (str)
        '''

        installation_directory = str(installation_directory)
        UtilityMethods.TYPE.InitialiseApiAccess(installation_directory if installation_directory else None)

    @staticmethod
    def initialise_dot_net_program_access():
        ''' 'InitialiseDotNetProgramAccess' is the original name of this method.'''

        UtilityMethods.TYPE.InitialiseDotNetProgramAccess()
