﻿'''_4390.py

ConceptCouplingCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2256
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4262
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4401
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ConceptCouplingCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundModalAnalysisAtAStiffness',)


class ConceptCouplingCompoundModalAnalysisAtAStiffness(_4401.CouplingCompoundModalAnalysisAtAStiffness):
    '''ConceptCouplingCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2256.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2256.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2256.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2256.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4262.ConceptCouplingModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingModalAnalysisAtAStiffness]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4262.ConceptCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4262.ConceptCouplingModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingModalAnalysisAtAStiffness]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4262.ConceptCouplingModalAnalysisAtAStiffness))
        return value
