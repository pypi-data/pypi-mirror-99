﻿'''_6102.py

FEPartCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5973
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6048
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'FEPartCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundDynamicAnalysis',)


class FEPartCompoundDynamicAnalysis(_6048.AbstractShaftOrHousingCompoundDynamicAnalysis):
    '''FEPartCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2130.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5973.FEPartDynamicAnalysis]':
        '''List[FEPartDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5973.FEPartDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundDynamicAnalysis]':
        '''List[FEPartCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5973.FEPartDynamicAnalysis]':
        '''List[FEPartDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5973.FEPartDynamicAnalysis))
        return value
