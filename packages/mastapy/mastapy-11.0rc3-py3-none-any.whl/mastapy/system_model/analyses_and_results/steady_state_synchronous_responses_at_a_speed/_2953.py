﻿'''_2953.py

CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2018
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6495
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2911
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed',)


class CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed(_2911.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed):
    '''CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2018.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6495.CycloidalDiscPlanetaryBearingConnectionLoadCase':
        '''CycloidalDiscPlanetaryBearingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6495.CycloidalDiscPlanetaryBearingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
