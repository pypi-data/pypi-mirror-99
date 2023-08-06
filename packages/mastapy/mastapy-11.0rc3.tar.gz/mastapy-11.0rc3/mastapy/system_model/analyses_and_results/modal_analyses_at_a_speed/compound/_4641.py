﻿'''_4641.py

BoltCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4513
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4647
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'BoltCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundModalAnalysisAtASpeed',)


class BoltCompoundModalAnalysisAtASpeed(_4647.ComponentCompoundModalAnalysisAtASpeed):
    '''BoltCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4513.BoltModalAnalysisAtASpeed]':
        '''List[BoltModalAnalysisAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4513.BoltModalAnalysisAtASpeed))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4513.BoltModalAnalysisAtASpeed]':
        '''List[BoltModalAnalysisAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4513.BoltModalAnalysisAtASpeed))
        return value
