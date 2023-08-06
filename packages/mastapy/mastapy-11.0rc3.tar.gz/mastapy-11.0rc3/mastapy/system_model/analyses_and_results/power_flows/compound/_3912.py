﻿'''_3912.py

PlanetaryConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1967
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3780
from mastapy.system_model.analyses_and_results.power_flows.compound import _3926
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PlanetaryConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundPowerFlow',)


class PlanetaryConnectionCompoundPowerFlow(_3926.ShaftToMountableComponentConnectionCompoundPowerFlow):
    '''PlanetaryConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1967.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1967.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1967.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1967.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3780.PlanetaryConnectionPowerFlow]':
        '''List[PlanetaryConnectionPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3780.PlanetaryConnectionPowerFlow))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3780.PlanetaryConnectionPowerFlow]':
        '''List[PlanetaryConnectionPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3780.PlanetaryConnectionPowerFlow))
        return value
