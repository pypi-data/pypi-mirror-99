﻿'''_2137.py

KlingelnbergCycloPalloidHypoidGearSet
'''


from typing import List

from mastapy.gears.gear_designs.klingelnberg_hypoid import _744
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2136, _2135
from mastapy.system_model.connections_and_sockets.gears import _1936
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSet',)


class KlingelnbergCycloPalloidHypoidGearSet(_2135.KlingelnbergCycloPalloidConicalGearSet):
    '''KlingelnbergCycloPalloidHypoidGearSet

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def klingelnberg_conical_gear_set_design(self) -> '_744.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'KlingelnbergConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_744.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.KlingelnbergConicalGearSetDesign) if self.wrapped.KlingelnbergConicalGearSetDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_744.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'KlingelnbergCycloPalloidHypoidGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_744.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.KlingelnbergCycloPalloidHypoidGearSetDesign) if self.wrapped.KlingelnbergCycloPalloidHypoidGearSetDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears(self) -> 'List[_2136.KlingelnbergCycloPalloidHypoidGear]':
        '''List[KlingelnbergCycloPalloidHypoidGear]: 'KlingelnbergCycloPalloidHypoidGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGears, constructor.new(_2136.KlingelnbergCycloPalloidHypoidGear))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes(self) -> 'List[_1936.KlingelnbergCycloPalloidHypoidGearMesh]':
        '''List[KlingelnbergCycloPalloidHypoidGearMesh]: 'KlingelnbergCycloPalloidHypoidMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshes, constructor.new(_1936.KlingelnbergCycloPalloidHypoidGearMesh))
        return value
