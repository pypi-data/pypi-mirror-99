﻿'''_6627.py

ZerolBevelGearMeshLoadCase
'''


from mastapy.system_model.connections_and_sockets.gears import _2011
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6464
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshLoadCase',)


class ZerolBevelGearMeshLoadCase(_6464.BevelGearMeshLoadCase):
    '''ZerolBevelGearMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2011.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
