﻿'''_6258.py

StraightBevelGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2145
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6132
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearLoadCase',)


class StraightBevelGearLoadCase(_6132.BevelGearLoadCase):
    '''StraightBevelGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
