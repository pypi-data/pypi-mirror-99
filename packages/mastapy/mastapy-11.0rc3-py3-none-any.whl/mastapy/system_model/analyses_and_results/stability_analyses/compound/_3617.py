﻿'''_3617.py

FEPartCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3486
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3563
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'FEPartCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundStabilityAnalysis',)


class FEPartCompoundStabilityAnalysis(_3563.AbstractShaftOrHousingCompoundStabilityAnalysis):
    '''FEPartCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundStabilityAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_3486.FEPartStabilityAnalysis]':
        '''List[FEPartStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3486.FEPartStabilityAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundStabilityAnalysis]':
        '''List[FEPartCompoundStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3486.FEPartStabilityAnalysis]':
        '''List[FEPartStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3486.FEPartStabilityAnalysis))
        return value
