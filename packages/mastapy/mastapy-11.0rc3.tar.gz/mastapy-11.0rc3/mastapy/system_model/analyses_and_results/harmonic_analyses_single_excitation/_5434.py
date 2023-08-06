﻿'''_5434.py

SpiralBevelGearHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.gears import _2218
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6592
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5350
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'SpiralBevelGearHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearHarmonicAnalysisOfSingleExcitation',)


class SpiralBevelGearHarmonicAnalysisOfSingleExcitation(_5350.BevelGearHarmonicAnalysisOfSingleExcitation):
    '''SpiralBevelGearHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearHarmonicAnalysisOfSingleExcitation.TYPE'):
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
    def component_load_case(self) -> '_6592.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6592.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
