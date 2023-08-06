﻿'''_3953.py

ConceptCouplingParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2227
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6438
from mastapy.system_model.analyses_and_results.system_deflections import _2354
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3964
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ConceptCouplingParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingParametricStudyTool',)


class ConceptCouplingParametricStudyTool(_3964.CouplingParametricStudyTool):
    '''ConceptCouplingParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2227.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2227.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6438.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6438.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2354.ConceptCouplingSystemDeflection]':
        '''List[ConceptCouplingSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2354.ConceptCouplingSystemDeflection))
        return value
