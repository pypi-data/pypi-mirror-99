﻿'''_4441.py

MountableComponentCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4312
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4389
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'MountableComponentCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundModalAnalysisAtAStiffness',)


class MountableComponentCompoundModalAnalysisAtAStiffness(_4389.ComponentCompoundModalAnalysisAtAStiffness):
    '''MountableComponentCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_4312.MountableComponentModalAnalysisAtAStiffness]':
        '''List[MountableComponentModalAnalysisAtAStiffness]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4312.MountableComponentModalAnalysisAtAStiffness))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4312.MountableComponentModalAnalysisAtAStiffness]':
        '''List[MountableComponentModalAnalysisAtAStiffness]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4312.MountableComponentModalAnalysisAtAStiffness))
        return value
