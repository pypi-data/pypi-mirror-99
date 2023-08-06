﻿'''_3063.py

ComponentCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2933
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3117
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'ComponentCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundSteadyStateSynchronousResponseAtASpeed',)


class ComponentCompoundSteadyStateSynchronousResponseAtASpeed(_3117.PartCompoundSteadyStateSynchronousResponseAtASpeed):
    '''ComponentCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_2933.ComponentSteadyStateSynchronousResponseAtASpeed]':
        '''List[ComponentSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2933.ComponentSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_2933.ComponentSteadyStateSynchronousResponseAtASpeed]':
        '''List[ComponentSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2933.ComponentSteadyStateSynchronousResponseAtASpeed))
        return value
