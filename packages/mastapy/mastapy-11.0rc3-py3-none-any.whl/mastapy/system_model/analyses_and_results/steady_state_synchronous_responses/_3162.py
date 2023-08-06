﻿'''_3162.py

ConceptCouplingSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2227
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6438
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3173
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ConceptCouplingSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingSteadyStateSynchronousResponse',)


class ConceptCouplingSteadyStateSynchronousResponse(_3173.CouplingSteadyStateSynchronousResponse):
    '''ConceptCouplingSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2227.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2227.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6438.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6438.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
