﻿'''_3741.py

CycloidalDiscPlanetaryBearingConnectionPowerFlow
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2018
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6495
from mastapy.system_model.analyses_and_results.power_flows import _3699
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CycloidalDiscPlanetaryBearingConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionPowerFlow',)


class CycloidalDiscPlanetaryBearingConnectionPowerFlow(_3699.AbstractShaftToMountableComponentConnectionPowerFlow):
    '''CycloidalDiscPlanetaryBearingConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionPowerFlow.TYPE'):
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
