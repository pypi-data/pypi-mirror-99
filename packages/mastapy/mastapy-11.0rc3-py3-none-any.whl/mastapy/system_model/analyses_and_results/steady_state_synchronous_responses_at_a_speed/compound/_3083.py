﻿'''_3083.py

CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2244
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2954
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3039
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed',)


class CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed(_3039.AbstractShaftCompoundSteadyStateSynchronousResponseAtASpeed):
    '''CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2244.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2954.CycloidalDiscSteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalDiscSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2954.CycloidalDiscSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2954.CycloidalDiscSteadyStateSynchronousResponseAtASpeed]':
        '''List[CycloidalDiscSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2954.CycloidalDiscSteadyStateSynchronousResponseAtASpeed))
        return value
