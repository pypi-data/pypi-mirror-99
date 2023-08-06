﻿'''_3925.py

ShaftHubConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2273
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3794
from mastapy.system_model.analyses_and_results.power_flows.compound import _3865
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ShaftHubConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundPowerFlow',)


class ShaftHubConnectionCompoundPowerFlow(_3865.ConnectorCompoundPowerFlow):
    '''ShaftHubConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2273.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3794.ShaftHubConnectionPowerFlow]':
        '''List[ShaftHubConnectionPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3794.ShaftHubConnectionPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3794.ShaftHubConnectionPowerFlow]':
        '''List[ShaftHubConnectionPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3794.ShaftHubConnectionPowerFlow))
        return value
