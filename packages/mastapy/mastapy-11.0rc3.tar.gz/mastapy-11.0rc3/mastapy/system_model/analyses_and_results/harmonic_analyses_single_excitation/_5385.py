﻿'''_5385.py

DatumHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6504
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5359
from mastapy._internal.python_net import python_net_import

_DATUM_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'DatumHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumHarmonicAnalysisOfSingleExcitation',)


class DatumHarmonicAnalysisOfSingleExcitation(_5359.ComponentHarmonicAnalysisOfSingleExcitation):
    '''DatumHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _DATUM_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2126.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6504.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
