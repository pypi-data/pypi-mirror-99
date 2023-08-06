﻿'''_707.py

StraightBevelGearSetParetoOptimiser
'''


from typing import List

from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.straight_bevel import _732
from mastapy.gears.gear_set_pareto_optimiser import _680

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_STRAIGHT_BEVEL_GEAR_SET_PARETO_OPTIMISER = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'StraightBevelGearSetParetoOptimiser')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetParetoOptimiser',)


class StraightBevelGearSetParetoOptimiser(_680.GearSetParetoOptimiser):
    '''StraightBevelGearSetParetoOptimiser

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_PARETO_OPTIMISER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetParetoOptimiser.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_space_search_strategy(self) -> 'str':
        '''str: 'DesignSpaceSearchStrategy' is the original name of this property.'''

        return self.wrapped.DesignSpaceSearchStrategy.SelectedItemName

    @design_space_search_strategy.setter
    def design_space_search_strategy(self, value: 'str'):
        self.wrapped.DesignSpaceSearchStrategy.SetSelectedItem(str(value) if value else None)

    @property
    def design_space_search_strategy_duty_cycle(self) -> 'str':
        '''str: 'DesignSpaceSearchStrategyDutyCycle' is the original name of this property.'''

        return self.wrapped.DesignSpaceSearchStrategyDutyCycle.SelectedItemName

    @design_space_search_strategy_duty_cycle.setter
    def design_space_search_strategy_duty_cycle(self, value: 'str'):
        self.wrapped.DesignSpaceSearchStrategyDutyCycle.SetSelectedItem(str(value) if value else None)

    @property
    def selected_candidate_geometry(self) -> '_732.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.StraightBevelGearSetDesign)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def candidate_gear_sets(self) -> 'List[_732.StraightBevelGearSetDesign]':
        '''List[StraightBevelGearSetDesign]: 'CandidateGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CandidateGearSets, constructor.new(_732.StraightBevelGearSetDesign))
        return value

    @property
    def all_candidate_gear_sets(self) -> 'List[_732.StraightBevelGearSetDesign]':
        '''List[StraightBevelGearSetDesign]: 'AllCandidateGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllCandidateGearSets, constructor.new(_732.StraightBevelGearSetDesign))
        return value
