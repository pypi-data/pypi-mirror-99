﻿'''_3051.py

BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2191
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3049, _3050, _3056
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2920
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed',)


class BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed(_3056.BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed):
    '''BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2191.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2191.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3049.BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialGearsCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3049.BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bevel_differential_meshes_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3050.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialMeshesCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3050.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2920.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2920.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2920.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2920.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed))
        return value
