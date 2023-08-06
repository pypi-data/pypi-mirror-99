﻿'''_3663.py

ZerolBevelGearParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2151
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6282
from mastapy.system_model.analyses_and_results.system_deflections import _2408
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3541
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ZerolBevelGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearParametricStudyTool',)


class ZerolBevelGearParametricStudyTool(_3541.BevelGearParametricStudyTool):
    '''ZerolBevelGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2151.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2151.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6282.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6282.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2408.ZerolBevelGearSystemDeflection]':
        '''List[ZerolBevelGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2408.ZerolBevelGearSystemDeflection))
        return value
