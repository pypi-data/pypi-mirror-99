﻿'''_2907.py

ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2229
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2905, _2906, _2797
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2777
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft',)


class ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft(_2797.BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft):
    '''ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2229.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2229.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2905.ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft]: 'ZerolBevelGearsCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_2905.ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def zerol_bevel_meshes_compound_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2906.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft]: 'ZerolBevelMeshesCompoundSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundSteadyStateSynchronousResponseOnAShaft, constructor.new(_2906.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2777.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2777.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2777.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2777.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value
