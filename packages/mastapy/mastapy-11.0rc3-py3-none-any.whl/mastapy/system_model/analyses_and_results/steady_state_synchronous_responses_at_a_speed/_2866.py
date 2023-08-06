﻿'''_2866.py

PowerLoadSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model import _2072
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6236
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2900
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'PowerLoadSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadSteadyStateSynchronousResponseAtASpeed',)


class PowerLoadSteadyStateSynchronousResponseAtASpeed(_2900.VirtualComponentSteadyStateSynchronousResponseAtASpeed):
    '''PowerLoadSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2072.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2072.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6236.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6236.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
