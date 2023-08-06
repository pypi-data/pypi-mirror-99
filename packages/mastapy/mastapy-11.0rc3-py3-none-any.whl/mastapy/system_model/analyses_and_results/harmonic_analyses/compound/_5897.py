﻿'''_5897.py

TorqueConverterPumpCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2283
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5740
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5817
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'TorqueConverterPumpCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundHarmonicAnalysis',)


class TorqueConverterPumpCompoundHarmonicAnalysis(_5817.CouplingHalfCompoundHarmonicAnalysis):
    '''TorqueConverterPumpCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundHarmonicAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_5740.TorqueConverterPumpHarmonicAnalysis]':
        '''List[TorqueConverterPumpHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5740.TorqueConverterPumpHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5740.TorqueConverterPumpHarmonicAnalysis]':
        '''List[TorqueConverterPumpHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5740.TorqueConverterPumpHarmonicAnalysis))
        return value
