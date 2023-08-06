﻿'''_1505.py

DynamicsResponseScaling
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DYNAMICS_RESPONSE_SCALING = python_net_import('SMT.MastaAPI.MathUtility', 'DynamicsResponseScaling')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicsResponseScaling',)


class DynamicsResponseScaling(Enum):
    '''DynamicsResponseScaling

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DYNAMICS_RESPONSE_SCALING

    __hash__ = None

    NO_SCALING = 0
    LOG_BASE_10 = 1
    DECIBEL = 2


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


DynamicsResponseScaling.__setattr__ = __enum_setattr
DynamicsResponseScaling.__delattr__ = __enum_delattr
