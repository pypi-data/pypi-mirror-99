﻿'''_4393.py

ConceptGearCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4264
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4422
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ConceptGearCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundModalAnalysisAtAStiffness',)


class ConceptGearCompoundModalAnalysisAtAStiffness(_4422.GearCompoundModalAnalysisAtAStiffness):
    '''ConceptGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4264.ConceptGearModalAnalysisAtAStiffness]':
        '''List[ConceptGearModalAnalysisAtAStiffness]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4264.ConceptGearModalAnalysisAtAStiffness))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4264.ConceptGearModalAnalysisAtAStiffness]':
        '''List[ConceptGearModalAnalysisAtAStiffness]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4264.ConceptGearModalAnalysisAtAStiffness))
        return value
