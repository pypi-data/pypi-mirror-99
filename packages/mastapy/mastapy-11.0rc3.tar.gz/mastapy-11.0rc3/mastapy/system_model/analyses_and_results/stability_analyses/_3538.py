﻿'''_3538.py

StraightBevelDiffGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2221
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6601
from mastapy.system_model.analyses_and_results.stability_analyses import _3539, _3537, _3446
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'StraightBevelDiffGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetStabilityAnalysis',)


class StraightBevelDiffGearSetStabilityAnalysis(_3446.BevelGearSetStabilityAnalysis):
    '''StraightBevelDiffGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2221.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6601.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6601.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_stability_analysis(self) -> 'List[_3539.StraightBevelDiffGearStabilityAnalysis]':
        '''List[StraightBevelDiffGearStabilityAnalysis]: 'StraightBevelDiffGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsStabilityAnalysis, constructor.new(_3539.StraightBevelDiffGearStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_stability_analysis(self) -> 'List[_3537.StraightBevelDiffGearMeshStabilityAnalysis]':
        '''List[StraightBevelDiffGearMeshStabilityAnalysis]: 'StraightBevelDiffMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesStabilityAnalysis, constructor.new(_3537.StraightBevelDiffGearMeshStabilityAnalysis))
        return value
