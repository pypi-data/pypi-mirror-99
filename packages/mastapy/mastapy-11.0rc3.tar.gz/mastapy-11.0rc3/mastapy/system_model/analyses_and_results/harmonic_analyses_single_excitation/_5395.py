﻿'''_5395.py

GuideDxfModelHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model import _2132
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6532
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5359
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'GuideDxfModelHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelHarmonicAnalysisOfSingleExcitation',)


class GuideDxfModelHarmonicAnalysisOfSingleExcitation(_5359.ComponentHarmonicAnalysisOfSingleExcitation):
    '''GuideDxfModelHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2132.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6532.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6532.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
