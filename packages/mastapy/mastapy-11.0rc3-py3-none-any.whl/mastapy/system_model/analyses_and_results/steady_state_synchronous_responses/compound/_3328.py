﻿'''_3328.py

ConceptCouplingHalfCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2257
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3194
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3339
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ConceptCouplingHalfCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundSteadyStateSynchronousResponse',)


class ConceptCouplingHalfCompoundSteadyStateSynchronousResponse(_3339.CouplingHalfCompoundSteadyStateSynchronousResponse):
    '''ConceptCouplingHalfCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2257.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2257.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3194.ConceptCouplingHalfSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingHalfSteadyStateSynchronousResponse]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3194.ConceptCouplingHalfSteadyStateSynchronousResponse))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3194.ConceptCouplingHalfSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingHalfSteadyStateSynchronousResponse]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3194.ConceptCouplingHalfSteadyStateSynchronousResponse))
        return value
