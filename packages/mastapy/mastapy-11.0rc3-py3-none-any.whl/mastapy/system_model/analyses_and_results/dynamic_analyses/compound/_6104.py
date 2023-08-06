﻿'''_6104.py

GearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.dynamic_analyses import _5975
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6123
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'GearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundDynamicAnalysis',)


class GearCompoundDynamicAnalysis(_6123.MountableComponentCompoundDynamicAnalysis):
    '''GearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_5975.GearDynamicAnalysis]':
        '''List[GearDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5975.GearDynamicAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_5975.GearDynamicAnalysis]':
        '''List[GearDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5975.GearDynamicAnalysis))
        return value
