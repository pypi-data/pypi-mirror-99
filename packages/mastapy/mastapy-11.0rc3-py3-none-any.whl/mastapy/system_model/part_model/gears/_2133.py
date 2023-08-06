﻿'''_2133.py

HypoidGearSet
'''


from typing import List

from mastapy.gears.gear_designs.hypoid import _752
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2132, _2112
from mastapy.system_model.connections_and_sockets.gears import _1932
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSet',)


class HypoidGearSet(_2112.AGMAGleasonConicalGearSet):
    '''HypoidGearSet

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_gear_set_design(self) -> '_752.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_752.HypoidGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def hypoid_gear_set_design(self) -> '_752.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'HypoidGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_752.HypoidGearSetDesign)(self.wrapped.HypoidGearSetDesign) if self.wrapped.HypoidGearSetDesign else None

    @property
    def hypoid_gears(self) -> 'List[_2132.HypoidGear]':
        '''List[HypoidGear]: 'HypoidGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGears, constructor.new(_2132.HypoidGear))
        return value

    @property
    def hypoid_meshes(self) -> 'List[_1932.HypoidGearMesh]':
        '''List[HypoidGearMesh]: 'HypoidMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshes, constructor.new(_1932.HypoidGearMesh))
        return value
