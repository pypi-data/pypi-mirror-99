﻿'''_6111.py

BevelDifferentialSunGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2100
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6107
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelDifferentialSunGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearLoadCase',)


class BevelDifferentialSunGearLoadCase(_6107.BevelDifferentialGearLoadCase):
    '''BevelDifferentialSunGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2100.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2100.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
