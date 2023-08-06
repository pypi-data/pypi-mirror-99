﻿'''_1277.py

VelocitySmall
'''


from mastapy.utility.units_and_measurements import _1168
from mastapy._internal.python_net import python_net_import

_VELOCITY_SMALL = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'VelocitySmall')


__docformat__ = 'restructuredtext en'
__all__ = ('VelocitySmall',)


class VelocitySmall(_1168.MeasurementBase):
    '''VelocitySmall

    This is a mastapy class.
    '''

    TYPE = _VELOCITY_SMALL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VelocitySmall.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
