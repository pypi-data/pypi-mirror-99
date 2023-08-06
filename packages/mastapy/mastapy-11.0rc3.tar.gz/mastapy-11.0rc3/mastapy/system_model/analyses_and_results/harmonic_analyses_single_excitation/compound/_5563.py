﻿'''_5563.py

SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5434
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5480
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation',)


class SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation(_5480.BevelGearCompoundHarmonicAnalysisOfSingleExcitation):
    '''SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2218.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2218.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5434.SpiralBevelGearHarmonicAnalysisOfSingleExcitation]':
        '''List[SpiralBevelGearHarmonicAnalysisOfSingleExcitation]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5434.SpiralBevelGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5434.SpiralBevelGearHarmonicAnalysisOfSingleExcitation]':
        '''List[SpiralBevelGearHarmonicAnalysisOfSingleExcitation]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5434.SpiralBevelGearHarmonicAnalysisOfSingleExcitation))
        return value
