﻿'''_1353.py

DegreesMinutesSeconds
'''


from mastapy.utility.units_and_measurements import _1361
from mastapy._internal.python_net import python_net_import

_DEGREES_MINUTES_SECONDS = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'DegreesMinutesSeconds')


__docformat__ = 'restructuredtext en'
__all__ = ('DegreesMinutesSeconds',)


class DegreesMinutesSeconds(_1361.Unit):
    '''DegreesMinutesSeconds

    This is a mastapy class.
    '''

    TYPE = _DEGREES_MINUTES_SECONDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DegreesMinutesSeconds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
