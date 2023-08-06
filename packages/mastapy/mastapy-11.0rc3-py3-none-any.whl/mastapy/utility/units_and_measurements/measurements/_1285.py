﻿'''_1285.py

AngleVerySmall
'''


from mastapy.utility.units_and_measurements import _1274
from mastapy._internal.python_net import python_net_import

_ANGLE_VERY_SMALL = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'AngleVerySmall')


__docformat__ = 'restructuredtext en'
__all__ = ('AngleVerySmall',)


class AngleVerySmall(_1274.MeasurementBase):
    '''AngleVerySmall

    This is a mastapy class.
    '''

    TYPE = _ANGLE_VERY_SMALL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AngleVerySmall.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
