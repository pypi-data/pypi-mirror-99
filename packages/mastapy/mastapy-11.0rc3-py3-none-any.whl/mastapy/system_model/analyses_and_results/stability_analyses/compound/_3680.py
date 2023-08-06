﻿'''_3680.py

TorqueConverterPumpCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2283
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3550
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3600
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'TorqueConverterPumpCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundStabilityAnalysis',)


class TorqueConverterPumpCompoundStabilityAnalysis(_3600.CouplingHalfCompoundStabilityAnalysis):
    '''TorqueConverterPumpCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2283.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2283.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3550.TorqueConverterPumpStabilityAnalysis]':
        '''List[TorqueConverterPumpStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3550.TorqueConverterPumpStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3550.TorqueConverterPumpStabilityAnalysis]':
        '''List[TorqueConverterPumpStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3550.TorqueConverterPumpStabilityAnalysis))
        return value
