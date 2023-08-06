﻿'''_3472.py

KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1937
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3347
from mastapy.system_model.analyses_and_results.power_flows.compound import _3466
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow(_3466.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1937.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1937.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1937.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1937.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3347.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3347.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow))
        return value

    @property
    def connection_power_flow_load_cases(self) -> 'List[_3347.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow]: 'ConnectionPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionPowerFlowLoadCases, constructor.new(_3347.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow))
        return value
