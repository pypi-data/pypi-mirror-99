﻿'''_6715.py

HypoidGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2210
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6545
from mastapy.system_model.analyses_and_results.system_deflections import _2430
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6713, _6714, _6655
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'HypoidGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetAdvancedTimeSteppingAnalysisForModulation',)


class HypoidGearSetAdvancedTimeSteppingAnalysisForModulation(_6655.AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation):
    '''HypoidGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2210.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6545.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6545.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2430.HypoidGearSetSystemDeflection':
        '''HypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2430.HypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def hypoid_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6713.HypoidGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearAdvancedTimeSteppingAnalysisForModulation]: 'HypoidGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6713.HypoidGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def hypoid_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6714.HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'HypoidMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6714.HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
