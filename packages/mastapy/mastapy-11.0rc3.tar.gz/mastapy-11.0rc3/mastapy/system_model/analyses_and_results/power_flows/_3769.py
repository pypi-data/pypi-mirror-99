﻿'''_3769.py

KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _2000
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6557
from mastapy.gears.rating.klingelnberg_spiral_bevel import _366
from mastapy.system_model.analyses_and_results.power_flows import _3763
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow(_3763.KlingelnbergCycloPalloidConicalGearMeshPowerFlow):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2000.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2000.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6557.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6557.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_366.KlingelnbergCycloPalloidSpiralBevelGearMeshRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_366.KlingelnbergCycloPalloidSpiralBevelGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_366.KlingelnbergCycloPalloidSpiralBevelGearMeshRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_366.KlingelnbergCycloPalloidSpiralBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
