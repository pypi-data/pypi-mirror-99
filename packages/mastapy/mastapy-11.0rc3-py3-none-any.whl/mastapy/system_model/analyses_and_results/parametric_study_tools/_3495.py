﻿'''_3495.py

BeltDriveParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2133, _2142
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6085, _6118
from mastapy.system_model.analyses_and_results.system_deflections import _2238
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3594
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BeltDriveParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveParametricStudyTool',)


class BeltDriveParametricStudyTool(_3594.SpecialisedAssemblyParametricStudyTool):
    '''BeltDriveParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2133.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2133.BeltDrive.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BeltDrive. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6085.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6085.BeltDriveLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to BeltDriveLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2238.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2238.BeltDriveSystemDeflection))
        return value
