﻿'''_5746.py

WormGearMeshHarmonicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _2009
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6624
from mastapy.system_model.analyses_and_results.system_deflections import _2502
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5668
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'WormGearMeshHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshHarmonicAnalysis',)


class WormGearMeshHarmonicAnalysis(_5668.GearMeshHarmonicAnalysis):
    '''WormGearMeshHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2009.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6624.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6624.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2502.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2502.WormGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
