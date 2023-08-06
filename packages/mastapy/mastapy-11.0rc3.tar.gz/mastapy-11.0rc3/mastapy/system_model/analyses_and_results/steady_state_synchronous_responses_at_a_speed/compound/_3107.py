﻿'''_3107.py

KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2213
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2979
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3104
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed(_3104.KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseAtASpeed):
    '''KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2213.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2213.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2979.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2979.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2979.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2979.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed))
        return value
