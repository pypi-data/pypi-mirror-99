﻿'''_6154.py

StraightBevelGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2222
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6025
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6062
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'StraightBevelGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundDynamicAnalysis',)


class StraightBevelGearCompoundDynamicAnalysis(_6062.BevelGearCompoundDynamicAnalysis):
    '''StraightBevelGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2222.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2222.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6025.StraightBevelGearDynamicAnalysis]':
        '''List[StraightBevelGearDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6025.StraightBevelGearDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6025.StraightBevelGearDynamicAnalysis]':
        '''List[StraightBevelGearDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6025.StraightBevelGearDynamicAnalysis))
        return value
