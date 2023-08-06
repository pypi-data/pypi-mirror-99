﻿'''_4478.py

SynchroniserHalfCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2279
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4348
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4479
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'SynchroniserHalfCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundModalAnalysisAtAStiffness',)


class SynchroniserHalfCompoundModalAnalysisAtAStiffness(_4479.SynchroniserPartCompoundModalAnalysisAtAStiffness):
    '''SynchroniserHalfCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2279.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2279.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4348.SynchroniserHalfModalAnalysisAtAStiffness]':
        '''List[SynchroniserHalfModalAnalysisAtAStiffness]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4348.SynchroniserHalfModalAnalysisAtAStiffness))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4348.SynchroniserHalfModalAnalysisAtAStiffness]':
        '''List[SynchroniserHalfModalAnalysisAtAStiffness]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4348.SynchroniserHalfModalAnalysisAtAStiffness))
        return value
