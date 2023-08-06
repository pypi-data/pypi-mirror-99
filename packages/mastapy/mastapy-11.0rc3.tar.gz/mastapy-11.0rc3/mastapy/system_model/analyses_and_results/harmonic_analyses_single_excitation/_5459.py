﻿'''_5459.py

WormGearMeshHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.connections_and_sockets.gears import _2009
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6624
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5393
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'WormGearMeshHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshHarmonicAnalysisOfSingleExcitation',)


class WormGearMeshHarmonicAnalysisOfSingleExcitation(_5393.GearMeshHarmonicAnalysisOfSingleExcitation):
    '''WormGearMeshHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshHarmonicAnalysisOfSingleExcitation.TYPE'):
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
