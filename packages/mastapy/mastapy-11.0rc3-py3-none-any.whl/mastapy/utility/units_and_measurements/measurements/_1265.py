﻿'''_1265.py

Text
'''


from mastapy.utility.units_and_measurements import _1168
from mastapy._internal.python_net import python_net_import

_TEXT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Text')


__docformat__ = 'restructuredtext en'
__all__ = ('Text',)


class Text(_1168.MeasurementBase):
    '''Text

    This is a mastapy class.
    '''

    TYPE = _TEXT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Text.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
