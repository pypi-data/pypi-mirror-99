﻿'''_1802.py

SphericalRollerBearing
'''


from mastapy.bearings.bearing_designs.rolling import _1782
from mastapy._internal.python_net import python_net_import

_SPHERICAL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'SphericalRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('SphericalRollerBearing',)


class SphericalRollerBearing(_1782.BarrelRollerBearing):
    '''SphericalRollerBearing

    This is a mastapy class.
    '''

    TYPE = _SPHERICAL_ROLLER_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SphericalRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
