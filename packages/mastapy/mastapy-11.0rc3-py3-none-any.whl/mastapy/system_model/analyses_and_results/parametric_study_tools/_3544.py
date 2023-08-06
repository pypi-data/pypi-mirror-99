﻿'''_3544.py

BoltParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2044
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6136
from mastapy.system_model.analyses_and_results.system_deflections import _2287
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3549
from mastapy._internal.python_net import python_net_import

_BOLT_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BoltParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltParametricStudyTool',)


class BoltParametricStudyTool(_3549.ComponentParametricStudyTool):
    '''BoltParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BOLT_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2044.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2044.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6136.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6136.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2287.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2287.BoltSystemDeflection))
        return value
