﻿'''_1262.py

Temperature
'''


from mastapy.utility.units_and_measurements import _1168
from mastapy._internal.python_net import python_net_import

_TEMPERATURE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Temperature')


__docformat__ = 'restructuredtext en'
__all__ = ('Temperature',)


class Temperature(_1168.MeasurementBase):
    '''Temperature

    This is a mastapy class.
    '''

    TYPE = _TEMPERATURE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Temperature.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
