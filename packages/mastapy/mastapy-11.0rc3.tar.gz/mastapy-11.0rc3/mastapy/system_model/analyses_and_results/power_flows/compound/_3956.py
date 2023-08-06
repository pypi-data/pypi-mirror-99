﻿'''_3956.py

ZerolBevelGearMeshCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2011
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3826
from mastapy.system_model.analyses_and_results.power_flows.compound import _3846
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ZerolBevelGearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshCompoundPowerFlow',)


class ZerolBevelGearMeshCompoundPowerFlow(_3846.BevelGearMeshCompoundPowerFlow):
    '''ZerolBevelGearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2011.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.ZerolBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2011.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3826.ZerolBevelGearMeshPowerFlow]':
        '''List[ZerolBevelGearMeshPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3826.ZerolBevelGearMeshPowerFlow))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3826.ZerolBevelGearMeshPowerFlow]':
        '''List[ZerolBevelGearMeshPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3826.ZerolBevelGearMeshPowerFlow))
        return value
