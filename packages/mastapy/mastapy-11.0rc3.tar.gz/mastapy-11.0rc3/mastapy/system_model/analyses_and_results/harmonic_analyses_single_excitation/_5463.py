﻿'''_5463.py

ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2229
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6628
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5461, _5462, _5352
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation',)


class ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation(_5352.BevelGearSetHarmonicAnalysisOfSingleExcitation):
    '''ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2229.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6628.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6628.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_harmonic_analysis_of_single_excitation(self) -> 'List[_5461.ZerolBevelGearHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelGearsHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsHarmonicAnalysisOfSingleExcitation, constructor.new(_5461.ZerolBevelGearHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def zerol_bevel_meshes_harmonic_analysis_of_single_excitation(self) -> 'List[_5462.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelMeshesHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesHarmonicAnalysisOfSingleExcitation, constructor.new(_5462.ZerolBevelGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
