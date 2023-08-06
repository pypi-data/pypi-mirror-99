﻿'''_2090.py

FaceGearSet
'''


from typing import List

from mastapy.gears.gear_designs.face import _759
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2089, _2093
from mastapy.system_model.connections_and_sockets.gears import _1891
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSet',)


class FaceGearSet(_2093.GearSet):
    '''FaceGearSet

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_set_design(self) -> '_759.FaceGearSetDesign':
        '''FaceGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_759.FaceGearSetDesign)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign else None

    @property
    def face_gear_set_design(self) -> '_759.FaceGearSetDesign':
        '''FaceGearSetDesign: 'FaceGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_759.FaceGearSetDesign)(self.wrapped.FaceGearSetDesign) if self.wrapped.FaceGearSetDesign else None

    @property
    def face_gears(self) -> 'List[_2089.FaceGear]':
        '''List[FaceGear]: 'FaceGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGears, constructor.new(_2089.FaceGear))
        return value

    @property
    def face_meshes(self) -> 'List[_1891.FaceGearMesh]':
        '''List[FaceGearMesh]: 'FaceMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshes, constructor.new(_1891.FaceGearMesh))
        return value
