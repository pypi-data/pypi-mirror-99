﻿'''_4982.py

OilSealCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2143
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4834
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4940
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'OilSealCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundModalAnalysis',)


class OilSealCompoundModalAnalysis(_4940.ConnectorCompoundModalAnalysis):
    '''OilSealCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundModalAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_4834.OilSealModalAnalysis]':
        '''List[OilSealModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4834.OilSealModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4834.OilSealModalAnalysis]':
        '''List[OilSealModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4834.OilSealModalAnalysis))
        return value
