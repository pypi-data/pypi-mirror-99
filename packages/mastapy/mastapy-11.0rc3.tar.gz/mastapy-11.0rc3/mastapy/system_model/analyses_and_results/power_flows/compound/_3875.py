﻿'''_3875.py

CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2018
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3741
from mastapy.system_model.analyses_and_results.power_flows.compound import _3832
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow',)


class CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow(_3832.AbstractShaftToMountableComponentConnectionCompoundPowerFlow):
    '''CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2018.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2018.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3741.CycloidalDiscPlanetaryBearingConnectionPowerFlow]':
        '''List[CycloidalDiscPlanetaryBearingConnectionPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3741.CycloidalDiscPlanetaryBearingConnectionPowerFlow))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3741.CycloidalDiscPlanetaryBearingConnectionPowerFlow]':
        '''List[CycloidalDiscPlanetaryBearingConnectionPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3741.CycloidalDiscPlanetaryBearingConnectionPowerFlow))
        return value
