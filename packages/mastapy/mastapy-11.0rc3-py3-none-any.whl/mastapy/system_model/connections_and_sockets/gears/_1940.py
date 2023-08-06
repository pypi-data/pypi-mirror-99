﻿'''_1940.py

SpiralBevelGearMesh
'''


from mastapy.gears.gear_designs.spiral_bevel import _735
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _1920
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMesh',)


class SpiralBevelGearMesh(_1920.BevelGearMesh):
    '''SpiralBevelGearMesh

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_mesh_design(self) -> '_735.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_735.SpiralBevelGearMeshDesign)(self.wrapped.BevelGearMeshDesign) if self.wrapped.BevelGearMeshDesign else None

    @property
    def spiral_bevel_gear_mesh_design(self) -> '_735.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'SpiralBevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_735.SpiralBevelGearMeshDesign)(self.wrapped.SpiralBevelGearMeshDesign) if self.wrapped.SpiralBevelGearMeshDesign else None
