﻿'''_1747.py

LoadedThreePointContactBallBearingElement
'''


from mastapy.bearings.bearing_results.rolling import _1715
from mastapy._internal.python_net import python_net_import

_LOADED_THREE_POINT_CONTACT_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedThreePointContactBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedThreePointContactBallBearingElement',)


class LoadedThreePointContactBallBearingElement(_1715.LoadedMultiPointContactBallBearingElement):
    '''LoadedThreePointContactBallBearingElement

    This is a mastapy class.
    '''

    TYPE = _LOADED_THREE_POINT_CONTACT_BALL_BEARING_ELEMENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedThreePointContactBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
