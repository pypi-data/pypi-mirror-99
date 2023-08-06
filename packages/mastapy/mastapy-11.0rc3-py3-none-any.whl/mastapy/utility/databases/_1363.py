﻿'''_1363.py

SQLDatabase
'''


from typing import Generic, TypeVar

from mastapy.utility.databases import _1361, _1358, _1357
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SQL_DATABASE = python_net_import('SMT.MastaAPI.Utility.Databases', 'SQLDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('SQLDatabase',)


TKey = TypeVar('TKey', bound='_1358.DatabaseKey')
TValue = TypeVar('TValue', bound='_0.APIBase')


class SQLDatabase(_1357.Database['TKey', 'TValue'], Generic[TKey, TValue]):
    '''SQLDatabase

    This is a mastapy class.

    Generic Types:
        TKey
        TValue
    '''

    TYPE = _SQL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SQLDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def save(self, item: '_1361.NamedDatabaseItem'):
        ''' 'Save' is the original name of this method.

        Args:
            item (mastapy.utility.databases.NamedDatabaseItem)
        '''

        self.wrapped.Save(item.wrapped if item else None)

    def delete(self, key: '_1358.DatabaseKey'):
        ''' 'Delete' is the original name of this method.

        Args:
            key (mastapy.utility.databases.DatabaseKey)
        '''

        self.wrapped.Delete(key.wrapped if key else None)
