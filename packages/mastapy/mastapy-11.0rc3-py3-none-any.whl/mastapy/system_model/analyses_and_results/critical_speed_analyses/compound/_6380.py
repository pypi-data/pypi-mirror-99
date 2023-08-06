﻿'''_6380.py

KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6251
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6346
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis',)


class KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis(_6346.ConicalGearSetCompoundCriticalSpeedAnalysis):
    '''KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self) -> 'List[_6251.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6251.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6251.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6251.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis))
        return value
