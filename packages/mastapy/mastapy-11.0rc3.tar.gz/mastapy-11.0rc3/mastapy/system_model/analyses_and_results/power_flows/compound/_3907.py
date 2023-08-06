﻿'''_3907.py

OilSealCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2143
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3775
from mastapy.system_model.analyses_and_results.power_flows.compound import _3865
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'OilSealCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundPowerFlow',)


class OilSealCompoundPowerFlow(_3865.ConnectorCompoundPowerFlow):
    '''OilSealCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2143.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2143.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3775.OilSealPowerFlow]':
        '''List[OilSealPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3775.OilSealPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3775.OilSealPowerFlow]':
        '''List[OilSealPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3775.OilSealPowerFlow))
        return value
