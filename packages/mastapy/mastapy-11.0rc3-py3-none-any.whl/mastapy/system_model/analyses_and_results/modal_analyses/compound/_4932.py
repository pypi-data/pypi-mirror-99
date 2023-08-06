﻿'''_4932.py

ConceptCouplingHalfCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2257
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4778
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4943
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConceptCouplingHalfCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundModalAnalysis',)


class ConceptCouplingHalfCompoundModalAnalysis(_4943.CouplingHalfCompoundModalAnalysis):
    '''ConceptCouplingHalfCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundModalAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_4778.ConceptCouplingHalfModalAnalysis]':
        '''List[ConceptCouplingHalfModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4778.ConceptCouplingHalfModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4778.ConceptCouplingHalfModalAnalysis]':
        '''List[ConceptCouplingHalfModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4778.ConceptCouplingHalfModalAnalysis))
        return value
