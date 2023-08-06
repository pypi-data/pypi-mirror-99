﻿'''_2935.py

ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2257
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6474
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2946
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed',)


class ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed(_2946.CouplingHalfSteadyStateSynchronousResponseAtASpeed):
    '''ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed.TYPE'):
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
    def component_load_case(self) -> '_6474.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6474.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
