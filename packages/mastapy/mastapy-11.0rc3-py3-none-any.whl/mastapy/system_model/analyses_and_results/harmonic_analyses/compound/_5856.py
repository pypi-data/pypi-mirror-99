﻿'''_5856.py

OilSealCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2143
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5696
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5814
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'OilSealCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundHarmonicAnalysis',)


class OilSealCompoundHarmonicAnalysis(_5814.ConnectorCompoundHarmonicAnalysis):
    '''OilSealCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundHarmonicAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_5696.OilSealHarmonicAnalysis]':
        '''List[OilSealHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5696.OilSealHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5696.OilSealHarmonicAnalysis]':
        '''List[OilSealHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5696.OilSealHarmonicAnalysis))
        return value
