﻿'''_6769.py

ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2168
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6767, _6768, _6798
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6639
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation',)


class ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation(_6798.GearSetCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2168.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2168.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2168.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2168.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6767.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearsCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6767.ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_meshes_compound_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6768.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'ConceptMeshesCompoundAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6768.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6639.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6639.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def assembly_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6639.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]: 'AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6639.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
