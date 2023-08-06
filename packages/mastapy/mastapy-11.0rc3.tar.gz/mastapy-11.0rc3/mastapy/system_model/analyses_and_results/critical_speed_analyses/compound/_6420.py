﻿'''_6420.py

StraightBevelGearCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2222
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6291
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6328
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'StraightBevelGearCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundCriticalSpeedAnalysis',)


class StraightBevelGearCompoundCriticalSpeedAnalysis(_6328.BevelGearCompoundCriticalSpeedAnalysis):
    '''StraightBevelGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundCriticalSpeedAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_6291.StraightBevelGearCriticalSpeedAnalysis]':
        '''List[StraightBevelGearCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6291.StraightBevelGearCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6291.StraightBevelGearCriticalSpeedAnalysis]':
        '''List[StraightBevelGearCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6291.StraightBevelGearCriticalSpeedAnalysis))
        return value
