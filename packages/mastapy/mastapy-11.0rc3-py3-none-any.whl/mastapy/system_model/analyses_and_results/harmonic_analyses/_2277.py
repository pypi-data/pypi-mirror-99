﻿'''_2277.py

HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses import _2276
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_FOR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation',)


class HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation(_2276.HarmonicAnalysis):
    '''HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_ANALYSIS_FOR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
