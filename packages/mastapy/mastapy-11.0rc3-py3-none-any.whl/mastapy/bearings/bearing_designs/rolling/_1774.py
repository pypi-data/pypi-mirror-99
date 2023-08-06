﻿'''_1774.py

AngularContactBallBearing
'''


from mastapy.bearings.bearing_designs.rolling import _1779
from mastapy._internal.python_net import python_net_import

_ANGULAR_CONTACT_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'AngularContactBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('AngularContactBallBearing',)


class AngularContactBallBearing(_1779.BallBearing):
    '''AngularContactBallBearing

    This is a mastapy class.
    '''

    TYPE = _ANGULAR_CONTACT_BALL_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AngularContactBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
