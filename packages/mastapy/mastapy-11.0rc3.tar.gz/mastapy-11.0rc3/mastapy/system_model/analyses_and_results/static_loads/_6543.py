﻿'''_6543.py

HypoidGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6449
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HypoidGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearLoadCase',)


class HypoidGearLoadCase(_6449.AGMAGleasonConicalGearLoadCase):
    '''HypoidGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2209.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
