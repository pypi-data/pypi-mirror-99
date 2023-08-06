﻿'''_3881.py

ExternalCADModelCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2129
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3749
from mastapy.system_model.analyses_and_results.power_flows.compound import _3854
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ExternalCADModelCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundPowerFlow',)


class ExternalCADModelCompoundPowerFlow(_3854.ComponentCompoundPowerFlow):
    '''ExternalCADModelCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2129.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2129.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3749.ExternalCADModelPowerFlow]':
        '''List[ExternalCADModelPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3749.ExternalCADModelPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3749.ExternalCADModelPowerFlow]':
        '''List[ExternalCADModelPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3749.ExternalCADModelPowerFlow))
        return value
