﻿'''_6212.py

ConceptGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2197
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6478
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6210, _6211, _6243
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'ConceptGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCriticalSpeedAnalysis',)


class ConceptGearSetCriticalSpeedAnalysis(_6243.GearSetCriticalSpeedAnalysis):
    '''ConceptGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2197.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2197.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6478.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6478.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_critical_speed_analysis(self) -> 'List[_6210.ConceptGearCriticalSpeedAnalysis]':
        '''List[ConceptGearCriticalSpeedAnalysis]: 'ConceptGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCriticalSpeedAnalysis, constructor.new(_6210.ConceptGearCriticalSpeedAnalysis))
        return value

    @property
    def concept_meshes_critical_speed_analysis(self) -> 'List[_6211.ConceptGearMeshCriticalSpeedAnalysis]':
        '''List[ConceptGearMeshCriticalSpeedAnalysis]: 'ConceptMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCriticalSpeedAnalysis, constructor.new(_6211.ConceptGearMeshCriticalSpeedAnalysis))
        return value
