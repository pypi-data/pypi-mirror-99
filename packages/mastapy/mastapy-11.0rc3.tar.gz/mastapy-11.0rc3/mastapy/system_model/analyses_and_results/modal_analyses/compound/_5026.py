﻿'''_5026.py

VirtualComponentCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import _4880
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4981
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'VirtualComponentCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundModalAnalysis',)


class VirtualComponentCompoundModalAnalysis(_4981.MountableComponentCompoundModalAnalysis):
    '''VirtualComponentCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_4880.VirtualComponentModalAnalysis]':
        '''List[VirtualComponentModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4880.VirtualComponentModalAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4880.VirtualComponentModalAnalysis]':
        '''List[VirtualComponentModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4880.VirtualComponentModalAnalysis))
        return value
