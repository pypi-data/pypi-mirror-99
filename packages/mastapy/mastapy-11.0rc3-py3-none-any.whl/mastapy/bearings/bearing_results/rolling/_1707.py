﻿'''_1707.py

LoadedDeepGrooveBallBearingElement
'''


from mastapy.bearings.bearing_results.rolling import _1696
from mastapy._internal.python_net import python_net_import

_LOADED_DEEP_GROOVE_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedDeepGrooveBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedDeepGrooveBallBearingElement',)


class LoadedDeepGrooveBallBearingElement(_1696.LoadedBallBearingElement):
    '''LoadedDeepGrooveBallBearingElement

    This is a mastapy class.
    '''

    TYPE = _LOADED_DEEP_GROOVE_BALL_BEARING_ELEMENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedDeepGrooveBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
