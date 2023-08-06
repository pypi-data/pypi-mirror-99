﻿'''_1752.py

LoadedThrustBallBearingRow
'''


from mastapy.bearings.bearing_results.rolling import _1751, _1699
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_THRUST_BALL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedThrustBallBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedThrustBallBearingRow',)


class LoadedThrustBallBearingRow(_1699.LoadedBallBearingRow):
    '''LoadedThrustBallBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_THRUST_BALL_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedThrustBallBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1751.LoadedThrustBallBearingResults':
        '''LoadedThrustBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1751.LoadedThrustBallBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
