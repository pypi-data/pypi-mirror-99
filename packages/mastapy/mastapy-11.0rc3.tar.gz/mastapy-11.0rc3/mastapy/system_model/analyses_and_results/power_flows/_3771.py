﻿'''_3771.py

KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2216
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6558
from mastapy.gears.rating.klingelnberg_spiral_bevel import _368
from mastapy.system_model.analyses_and_results.power_flows import _3770, _3769, _3765
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow',)


class KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow(_3765.KlingelnbergCycloPalloidConicalGearSetPowerFlow):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2216.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2216.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6558.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6558.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_368.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_368.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3770.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3770.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_power_flow(self) -> 'List[_3770.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsPowerFlow, constructor.new(_3770.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3769.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3769.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_power_flow(self) -> 'List[_3769.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesPowerFlow, constructor.new(_3769.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow))
        return value
