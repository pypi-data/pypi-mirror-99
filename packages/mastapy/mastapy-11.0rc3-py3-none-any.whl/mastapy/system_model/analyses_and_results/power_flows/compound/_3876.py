﻿'''_3876.py

CylindricalGearCompoundPowerFlow
'''


from typing import List

from mastapy.gears.rating.cylindrical import _413
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2200, _2202
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows import _3745
from mastapy.system_model.analyses_and_results.power_flows.compound import _3887
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CylindricalGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundPowerFlow',)


class CylindricalGearCompoundPowerFlow(_3887.GearCompoundPowerFlow):
    '''CylindricalGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_413.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_413.CylindricalGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def cylindrical_gear_duty_cycle_rating(self) -> '_413.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'CylindricalGearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_413.CylindricalGearDutyCycleRating)(self.wrapped.CylindricalGearDutyCycleRating) if self.wrapped.CylindricalGearDutyCycleRating else None

    @property
    def component_design(self) -> '_2200.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3745.CylindricalGearPowerFlow]':
        '''List[CylindricalGearPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3745.CylindricalGearPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3745.CylindricalGearPowerFlow]':
        '''List[CylindricalGearPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3745.CylindricalGearPowerFlow))
        return value
