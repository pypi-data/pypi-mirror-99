﻿'''_5440.py

StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.gears import _2220, _2224, _2225
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6599, _6605, _6606
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5350
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation',)


class StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation(_5350.BevelGearHarmonicAnalysisOfSingleExcitation):
    '''StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2220.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2220.StraightBevelDiffGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6599.StraightBevelDiffGearLoadCase':
        '''StraightBevelDiffGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6599.StraightBevelDiffGearLoadCase.TYPE not in self.wrapped.ComponentLoadCase.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to StraightBevelDiffGearLoadCase. Expected: {}.'.format(self.wrapped.ComponentLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentLoadCase.__class__)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
