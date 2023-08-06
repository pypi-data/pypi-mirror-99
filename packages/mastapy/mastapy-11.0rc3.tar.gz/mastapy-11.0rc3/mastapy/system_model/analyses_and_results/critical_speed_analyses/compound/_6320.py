﻿'''_6320.py

BearingCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2118
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6189
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6348
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'BearingCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundCriticalSpeedAnalysis',)


class BearingCompoundCriticalSpeedAnalysis(_6348.ConnectorCompoundCriticalSpeedAnalysis):
    '''BearingCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2118.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2118.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6189.BearingCriticalSpeedAnalysis]':
        '''List[BearingCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6189.BearingCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundCriticalSpeedAnalysis]':
        '''List[BearingCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6189.BearingCriticalSpeedAnalysis]':
        '''List[BearingCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6189.BearingCriticalSpeedAnalysis))
        return value
