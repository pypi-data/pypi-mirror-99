﻿'''_5823.py

CycloidalDiscCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2244
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5640
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5779
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'CycloidalDiscCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundHarmonicAnalysis',)


class CycloidalDiscCompoundHarmonicAnalysis(_5779.AbstractShaftCompoundHarmonicAnalysis):
    '''CycloidalDiscCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2244.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5640.CycloidalDiscHarmonicAnalysis]':
        '''List[CycloidalDiscHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5640.CycloidalDiscHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5640.CycloidalDiscHarmonicAnalysis]':
        '''List[CycloidalDiscHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5640.CycloidalDiscHarmonicAnalysis))
        return value
