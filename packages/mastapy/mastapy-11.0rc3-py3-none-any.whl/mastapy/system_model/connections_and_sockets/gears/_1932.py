﻿'''_1932.py

HypoidGearMesh
'''


from mastapy.gears.gear_designs.hypoid import _751
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _1916
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMesh',)


class HypoidGearMesh(_1916.AGMAGleasonConicalGearMesh):
    '''HypoidGearMesh

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hypoid_gear_mesh_design(self) -> '_751.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'HypoidGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_751.HypoidGearMeshDesign)(self.wrapped.HypoidGearMeshDesign) if self.wrapped.HypoidGearMeshDesign else None
