﻿'''_1702.py

LoadedCrossedRollerBearingRow
'''


from mastapy.bearings.bearing_results.rolling import _1701, _1726
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_CROSSED_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCrossedRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCrossedRollerBearingRow',)


class LoadedCrossedRollerBearingRow(_1726.LoadedRollerBearingRow):
    '''LoadedCrossedRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_CROSSED_ROLLER_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedCrossedRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1701.LoadedCrossedRollerBearingResults':
        '''LoadedCrossedRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1701.LoadedCrossedRollerBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
