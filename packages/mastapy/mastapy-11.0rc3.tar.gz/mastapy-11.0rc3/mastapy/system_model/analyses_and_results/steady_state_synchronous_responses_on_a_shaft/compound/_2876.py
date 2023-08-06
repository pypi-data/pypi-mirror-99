﻿'''_2876.py

ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2746
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _2782
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft',)


class ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft(_2782.AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft):
    '''ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_2746.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_2746.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_2746.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_2746.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft))
        return value
