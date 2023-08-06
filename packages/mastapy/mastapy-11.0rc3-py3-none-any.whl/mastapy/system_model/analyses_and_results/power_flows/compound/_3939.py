﻿'''_3939.py

StraightBevelGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2223
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3937, _3938, _3847
from mastapy.system_model.analyses_and_results.power_flows import _3809
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'StraightBevelGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundPowerFlow',)


class StraightBevelGearSetCompoundPowerFlow(_3847.BevelGearSetCompoundPowerFlow):
    '''StraightBevelGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2223.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2223.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_power_flow(self) -> 'List[_3937.StraightBevelGearCompoundPowerFlow]':
        '''List[StraightBevelGearCompoundPowerFlow]: 'StraightBevelGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundPowerFlow, constructor.new(_3937.StraightBevelGearCompoundPowerFlow))
        return value

    @property
    def straight_bevel_meshes_compound_power_flow(self) -> 'List[_3938.StraightBevelGearMeshCompoundPowerFlow]':
        '''List[StraightBevelGearMeshCompoundPowerFlow]: 'StraightBevelMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundPowerFlow, constructor.new(_3938.StraightBevelGearMeshCompoundPowerFlow))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3809.StraightBevelGearSetPowerFlow]':
        '''List[StraightBevelGearSetPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3809.StraightBevelGearSetPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3809.StraightBevelGearSetPowerFlow]':
        '''List[StraightBevelGearSetPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3809.StraightBevelGearSetPowerFlow))
        return value
