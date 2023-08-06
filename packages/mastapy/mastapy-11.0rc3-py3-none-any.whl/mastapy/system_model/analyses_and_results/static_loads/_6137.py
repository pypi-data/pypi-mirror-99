﻿'''_6137.py

ClutchConnectionLoadCase
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.couplings import _1950
from mastapy.system_model.analyses_and_results.static_loads import _6155
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ClutchConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionLoadCase',)


class ClutchConnectionLoadCase(_6155.CouplingConnectionLoadCase):
    '''ClutchConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_initially_locked(self) -> 'bool':
        '''bool: 'IsInitiallyLocked' is the original name of this property.'''

        return self.wrapped.IsInitiallyLocked

    @is_initially_locked.setter
    def is_initially_locked(self, value: 'bool'):
        self.wrapped.IsInitiallyLocked = bool(value) if value else False

    @property
    def unlocked_clutch_linear_resistance_coefficient(self) -> 'float':
        '''float: 'UnlockedClutchLinearResistanceCoefficient' is the original name of this property.'''

        return self.wrapped.UnlockedClutchLinearResistanceCoefficient

    @unlocked_clutch_linear_resistance_coefficient.setter
    def unlocked_clutch_linear_resistance_coefficient(self, value: 'float'):
        self.wrapped.UnlockedClutchLinearResistanceCoefficient = float(value) if value else 0.0

    @property
    def use_fixed_update_time(self) -> 'bool':
        '''bool: 'UseFixedUpdateTime' is the original name of this property.'''

        return self.wrapped.UseFixedUpdateTime

    @use_fixed_update_time.setter
    def use_fixed_update_time(self, value: 'bool'):
        self.wrapped.UseFixedUpdateTime = bool(value) if value else False

    @property
    def clutch_initial_temperature(self) -> 'float':
        '''float: 'ClutchInitialTemperature' is the original name of this property.'''

        return self.wrapped.ClutchInitialTemperature

    @clutch_initial_temperature.setter
    def clutch_initial_temperature(self, value: 'float'):
        self.wrapped.ClutchInitialTemperature = float(value) if value else 0.0

    @property
    def connection_design(self) -> '_1950.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1950.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
