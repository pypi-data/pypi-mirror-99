﻿'''_1803.py

BearingNodePosition
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_NODE_POSITION = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Concept', 'BearingNodePosition')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingNodePosition',)


class BearingNodePosition(Enum):
    '''BearingNodePosition

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _BEARING_NODE_POSITION

    __hash__ = None

    CENTRE = 0
    LEFT_AND_RIGHT = 1
