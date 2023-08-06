﻿'''_3586.py

ComponentCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.stability_analyses import _3454
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3640
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ComponentCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundStabilityAnalysis',)


class ComponentCompoundStabilityAnalysis(_3640.PartCompoundStabilityAnalysis):
    '''ComponentCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_3454.ComponentStabilityAnalysis]':
        '''List[ComponentStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3454.ComponentStabilityAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_3454.ComponentStabilityAnalysis]':
        '''List[ComponentStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3454.ComponentStabilityAnalysis))
        return value
