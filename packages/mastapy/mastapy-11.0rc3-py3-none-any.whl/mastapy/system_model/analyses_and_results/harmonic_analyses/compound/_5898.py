﻿'''_5898.py

TorqueConverterTurbineCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2285
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5741
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5817
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'TorqueConverterTurbineCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundHarmonicAnalysis',)


class TorqueConverterTurbineCompoundHarmonicAnalysis(_5817.CouplingHalfCompoundHarmonicAnalysis):
    '''TorqueConverterTurbineCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2285.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2285.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5741.TorqueConverterTurbineHarmonicAnalysis]':
        '''List[TorqueConverterTurbineHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5741.TorqueConverterTurbineHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5741.TorqueConverterTurbineHarmonicAnalysis]':
        '''List[TorqueConverterTurbineHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5741.TorqueConverterTurbineHarmonicAnalysis))
        return value
