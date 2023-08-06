﻿'''_3391.py

RollingRingAssemblyCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2272
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3259
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3398
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'RollingRingAssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyCompoundSteadyStateSynchronousResponse',)


class RollingRingAssemblyCompoundSteadyStateSynchronousResponse(_3398.SpecialisedAssemblyCompoundSteadyStateSynchronousResponse):
    '''RollingRingAssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2272.RollingRingAssembly':
        '''RollingRingAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.RollingRingAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2272.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3259.RollingRingAssemblySteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3259.RollingRingAssemblySteadyStateSynchronousResponse))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3259.RollingRingAssemblySteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3259.RollingRingAssemblySteadyStateSynchronousResponse))
        return value
