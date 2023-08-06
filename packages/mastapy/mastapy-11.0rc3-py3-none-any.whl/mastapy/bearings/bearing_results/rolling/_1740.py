﻿'''_1740.py

LoadedSphericalRollerThrustBearingRow
'''


from mastapy.bearings.bearing_results.rolling import _1739, _1726
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_SPHERICAL_ROLLER_THRUST_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedSphericalRollerThrustBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedSphericalRollerThrustBearingRow',)


class LoadedSphericalRollerThrustBearingRow(_1726.LoadedRollerBearingRow):
    '''LoadedSphericalRollerThrustBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_SPHERICAL_ROLLER_THRUST_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedSphericalRollerThrustBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1739.LoadedSphericalRollerThrustBearingResults':
        '''LoadedSphericalRollerThrustBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1739.LoadedSphericalRollerThrustBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
