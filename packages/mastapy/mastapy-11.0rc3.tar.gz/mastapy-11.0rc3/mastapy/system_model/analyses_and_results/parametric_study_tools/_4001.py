﻿'''_4001.py

CycloidalAssemblyParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2243
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6492
from mastapy.system_model.analyses_and_results.system_deflections import _2403
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4074
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CycloidalAssemblyParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyParametricStudyTool',)


class CycloidalAssemblyParametricStudyTool(_4074.SpecialisedAssemblyParametricStudyTool):
    '''CycloidalAssemblyParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2243.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2243.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6492.CycloidalAssemblyLoadCase':
        '''CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6492.CycloidalAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2403.CycloidalAssemblySystemDeflection]':
        '''List[CycloidalAssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2403.CycloidalAssemblySystemDeflection))
        return value
