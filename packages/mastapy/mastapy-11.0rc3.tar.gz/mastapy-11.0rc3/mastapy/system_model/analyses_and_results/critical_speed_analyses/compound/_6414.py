﻿'''_6414.py

SpringDamperCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6286
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6349
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'SpringDamperCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundCriticalSpeedAnalysis',)


class SpringDamperCompoundCriticalSpeedAnalysis(_6349.CouplingCompoundCriticalSpeedAnalysis):
    '''SpringDamperCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2275.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2275.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6286.SpringDamperCriticalSpeedAnalysis]':
        '''List[SpringDamperCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6286.SpringDamperCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6286.SpringDamperCriticalSpeedAnalysis]':
        '''List[SpringDamperCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6286.SpringDamperCriticalSpeedAnalysis))
        return value
