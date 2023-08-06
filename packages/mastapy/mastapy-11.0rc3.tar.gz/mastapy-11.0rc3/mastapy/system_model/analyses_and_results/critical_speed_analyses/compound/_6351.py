﻿'''_6351.py

CouplingHalfCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6220
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6389
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CouplingHalfCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundCriticalSpeedAnalysis',)


class CouplingHalfCompoundCriticalSpeedAnalysis(_6389.MountableComponentCompoundCriticalSpeedAnalysis):
    '''CouplingHalfCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_6220.CouplingHalfCriticalSpeedAnalysis]':
        '''List[CouplingHalfCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6220.CouplingHalfCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_6220.CouplingHalfCriticalSpeedAnalysis]':
        '''List[CouplingHalfCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6220.CouplingHalfCriticalSpeedAnalysis))
        return value
