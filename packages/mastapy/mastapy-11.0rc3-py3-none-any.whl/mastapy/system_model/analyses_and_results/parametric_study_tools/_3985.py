﻿'''_3985.py

ConceptCouplingHalfParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2257
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6474
from mastapy.system_model.analyses_and_results.system_deflections import _2386
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3996
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ConceptCouplingHalfParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfParametricStudyTool',)


class ConceptCouplingHalfParametricStudyTool(_3996.CouplingHalfParametricStudyTool):
    '''ConceptCouplingHalfParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2257.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2257.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6474.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6474.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2386.ConceptCouplingHalfSystemDeflection]':
        '''List[ConceptCouplingHalfSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2386.ConceptCouplingHalfSystemDeflection))
        return value
