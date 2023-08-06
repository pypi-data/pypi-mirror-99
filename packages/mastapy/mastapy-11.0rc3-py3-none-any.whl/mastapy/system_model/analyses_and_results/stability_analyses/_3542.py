﻿'''_3542.py

StraightBevelGearStabilityAnalysis
'''


from mastapy.system_model.part_model.gears import _2222
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6602
from mastapy.system_model.analyses_and_results.stability_analyses import _3447
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'StraightBevelGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearStabilityAnalysis',)


class StraightBevelGearStabilityAnalysis(_3447.BevelGearStabilityAnalysis):
    '''StraightBevelGearStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2222.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2222.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6602.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6602.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
