﻿'''_5803.py

ComponentCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5620
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5857
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'ComponentCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundHarmonicAnalysis',)


class ComponentCompoundHarmonicAnalysis(_5857.PartCompoundHarmonicAnalysis):
    '''ComponentCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_5620.ComponentHarmonicAnalysis]':
        '''List[ComponentHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5620.ComponentHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_5620.ComponentHarmonicAnalysis]':
        '''List[ComponentHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5620.ComponentHarmonicAnalysis))
        return value
