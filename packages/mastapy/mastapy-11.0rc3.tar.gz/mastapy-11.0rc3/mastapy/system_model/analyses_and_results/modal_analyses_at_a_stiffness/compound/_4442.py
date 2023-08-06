﻿'''_4442.py

OilSealCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2143
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4313
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4400
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'OilSealCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundModalAnalysisAtAStiffness',)


class OilSealCompoundModalAnalysisAtAStiffness(_4400.ConnectorCompoundModalAnalysisAtAStiffness):
    '''OilSealCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2143.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2143.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4313.OilSealModalAnalysisAtAStiffness]':
        '''List[OilSealModalAnalysisAtAStiffness]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4313.OilSealModalAnalysisAtAStiffness))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4313.OilSealModalAnalysisAtAStiffness]':
        '''List[OilSealModalAnalysisAtAStiffness]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4313.OilSealModalAnalysisAtAStiffness))
        return value
