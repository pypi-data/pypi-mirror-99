﻿'''_4401.py

CouplingCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4273
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4462
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CouplingCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundModalAnalysisAtAStiffness',)


class CouplingCompoundModalAnalysisAtAStiffness(_4462.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness):
    '''CouplingCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self) -> 'List[_4273.CouplingModalAnalysisAtAStiffness]':
        '''List[CouplingModalAnalysisAtAStiffness]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4273.CouplingModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4273.CouplingModalAnalysisAtAStiffness]':
        '''List[CouplingModalAnalysisAtAStiffness]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4273.CouplingModalAnalysisAtAStiffness))
        return value
