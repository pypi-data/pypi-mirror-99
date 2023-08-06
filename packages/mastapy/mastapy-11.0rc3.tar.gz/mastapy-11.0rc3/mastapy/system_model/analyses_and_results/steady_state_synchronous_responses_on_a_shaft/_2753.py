﻿'''_2753.py

SpringDamperSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6597
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2688
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'SpringDamperSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperSteadyStateSynchronousResponseOnAShaft',)


class SpringDamperSteadyStateSynchronousResponseOnAShaft(_2688.CouplingSteadyStateSynchronousResponseOnAShaft):
    '''SpringDamperSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2275.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6597.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6597.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
