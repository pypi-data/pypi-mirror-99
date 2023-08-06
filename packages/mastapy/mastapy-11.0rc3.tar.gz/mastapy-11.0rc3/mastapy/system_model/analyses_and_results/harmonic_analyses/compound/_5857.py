﻿'''_5857.py

PartCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5697
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _7185
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'PartCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundHarmonicAnalysis',)


class PartCompoundHarmonicAnalysis(_7185.PartCompoundAnalysis):
    '''PartCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_5697.PartHarmonicAnalysis]':
        '''List[PartHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5697.PartHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_5697.PartHarmonicAnalysis]':
        '''List[PartHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5697.PartHarmonicAnalysis))
        return value
