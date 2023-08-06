﻿'''_2807.py

CoaxialConnectionSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.connections_and_sockets import _1889
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6140
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2874
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'CoaxialConnectionSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionSteadyStateSynchronousResponseAtASpeed',)


class CoaxialConnectionSteadyStateSynchronousResponseAtASpeed(_2874.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed):
    '''CoaxialConnectionSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1889.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1889.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6140.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6140.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
