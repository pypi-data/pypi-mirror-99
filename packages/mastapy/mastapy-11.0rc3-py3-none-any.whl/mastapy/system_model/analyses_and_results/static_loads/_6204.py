﻿'''_6204.py

HypoidGearMeshLoadCase
'''


from mastapy.system_model.connections_and_sockets.gears import _1932
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6120
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HypoidGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshLoadCase',)


class HypoidGearMeshLoadCase(_6120.AGMAGleasonConicalGearMeshLoadCase):
    '''HypoidGearMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1932.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
