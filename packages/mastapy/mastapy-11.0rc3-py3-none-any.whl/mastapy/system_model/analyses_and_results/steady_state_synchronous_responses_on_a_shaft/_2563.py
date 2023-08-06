﻿'''_2563.py

ClutchSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2172
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6139
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2579
from mastapy._internal.python_net import python_net_import

_CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'ClutchSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchSteadyStateSynchronousResponseOnAShaft',)


class ClutchSteadyStateSynchronousResponseOnAShaft(_2579.CouplingSteadyStateSynchronousResponseOnAShaft):
    '''ClutchSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2172.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2172.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6139.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6139.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
