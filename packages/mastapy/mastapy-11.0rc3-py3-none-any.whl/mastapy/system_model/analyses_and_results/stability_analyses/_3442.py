﻿'''_3442.py

BevelDifferentialGearStabilityAnalysis
'''


from mastapy.system_model.part_model.gears import _2190, _2192, _2193
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6458, _6461, _6462
from mastapy.system_model.analyses_and_results.stability_analyses import _3447
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'BevelDifferentialGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearStabilityAnalysis',)


class BevelDifferentialGearStabilityAnalysis(_3447.BevelGearStabilityAnalysis):
    '''BevelDifferentialGearStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2190.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.BevelDifferentialGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6458.BevelDifferentialGearLoadCase':
        '''BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6458.BevelDifferentialGearLoadCase.TYPE not in self.wrapped.ComponentLoadCase.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to BevelDifferentialGearLoadCase. Expected: {}.'.format(self.wrapped.ComponentLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentLoadCase.__class__)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
