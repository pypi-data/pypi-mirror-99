﻿'''_1891.py

FaceGearMesh
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.face import _755
from mastapy.system_model.connections_and_sockets.gears import _1893
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMesh',)


class FaceGearMesh(_1893.GearMesh):
    '''FaceGearMesh

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pinion_drop_angle(self) -> 'float':
        '''float: 'PinionDropAngle' is the original name of this property.'''

        return self.wrapped.PinionDropAngle

    @pinion_drop_angle.setter
    def pinion_drop_angle(self, value: 'float'):
        self.wrapped.PinionDropAngle = float(value) if value else 0.0

    @property
    def wheel_drop_angle(self) -> 'float':
        '''float: 'WheelDropAngle' is the original name of this property.'''

        return self.wrapped.WheelDropAngle

    @wheel_drop_angle.setter
    def wheel_drop_angle(self, value: 'float'):
        self.wrapped.WheelDropAngle = float(value) if value else 0.0

    @property
    def face_gear_mesh_design(self) -> '_755.FaceGearMeshDesign':
        '''FaceGearMeshDesign: 'FaceGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_755.FaceGearMeshDesign)(self.wrapped.FaceGearMeshDesign) if self.wrapped.FaceGearMeshDesign else None
