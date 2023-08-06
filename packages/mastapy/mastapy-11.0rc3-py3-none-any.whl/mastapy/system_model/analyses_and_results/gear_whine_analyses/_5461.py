﻿'''_5461.py

WormGearMeshGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1946
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6280
from mastapy.system_model.analyses_and_results.system_deflections import _2403
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5386
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'WormGearMeshGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshGearWhineAnalysis',)


class WormGearMeshGearWhineAnalysis(_5386.GearMeshGearWhineAnalysis):
    '''WormGearMeshGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1946.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1946.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6280.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6280.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2403.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2403.WormGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
