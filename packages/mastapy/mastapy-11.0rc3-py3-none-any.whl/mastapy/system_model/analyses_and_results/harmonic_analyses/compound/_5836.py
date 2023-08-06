﻿'''_5836.py

GearCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5666
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5855
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'GearCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundHarmonicAnalysis',)


class GearCompoundHarmonicAnalysis(_5855.MountableComponentCompoundHarmonicAnalysis):
    '''GearCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_5666.GearHarmonicAnalysis]':
        '''List[GearHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5666.GearHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_5666.GearHarmonicAnalysis]':
        '''List[GearHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5666.GearHarmonicAnalysis))
        return value
