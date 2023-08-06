﻿'''_4644.py

ClutchConnectionCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2022
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4514
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4660
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'ClutchConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundModalAnalysisAtASpeed',)


class ClutchConnectionCompoundModalAnalysisAtASpeed(_4660.CouplingConnectionCompoundModalAnalysisAtASpeed):
    '''ClutchConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2022.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2022.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4514.ClutchConnectionModalAnalysisAtASpeed]':
        '''List[ClutchConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_4514.ClutchConnectionModalAnalysisAtASpeed))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4514.ClutchConnectionModalAnalysisAtASpeed]':
        '''List[ClutchConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_4514.ClutchConnectionModalAnalysisAtASpeed))
        return value
