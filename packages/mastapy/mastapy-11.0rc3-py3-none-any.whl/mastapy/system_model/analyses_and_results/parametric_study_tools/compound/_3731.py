﻿'''_3731.py

KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2138
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3600
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3725
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool',)


class KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool(_3725.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool):
    '''KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2138.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3600.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3600.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3600.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3600.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool))
        return value
