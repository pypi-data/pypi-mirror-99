﻿'''_3038.py

AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2908
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3117
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed',)


class AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed(_3117.PartCompoundSteadyStateSynchronousResponseAtASpeed):
    '''AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self) -> 'List[_2908.AbstractAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[AbstractAssemblySteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2908.AbstractAssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2908.AbstractAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[AbstractAssemblySteadyStateSynchronousResponseAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2908.AbstractAssemblySteadyStateSynchronousResponseAtASpeed))
        return value
