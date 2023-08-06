﻿'''_908.py

KlingelnbergCycloPalloidHypoidGearMeshDesign
'''


from typing import List

from mastapy.gears.gear_designs.klingelnberg_hypoid import _909, _907, _910
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.klingelnberg_conical import _912
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergHypoid', 'KlingelnbergCycloPalloidHypoidGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshDesign',)


class KlingelnbergCycloPalloidHypoidGearMeshDesign(_912.KlingelnbergConicalGearMeshDesign):
    '''KlingelnbergCycloPalloidHypoidGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_909.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'KlingelnbergCycloPalloidHypoidGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_909.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.KlingelnbergCycloPalloidHypoidGearSet) if self.wrapped.KlingelnbergCycloPalloidHypoidGearSet else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears(self) -> 'List[_907.KlingelnbergCycloPalloidHypoidGearDesign]':
        '''List[KlingelnbergCycloPalloidHypoidGearDesign]: 'KlingelnbergCycloPalloidHypoidGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGears, constructor.new(_907.KlingelnbergCycloPalloidHypoidGearDesign))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshed_gears(self) -> 'List[_910.KlingelnbergCycloPalloidHypoidMeshedGearDesign]':
        '''List[KlingelnbergCycloPalloidHypoidMeshedGearDesign]: 'KlingelnbergCycloPalloidHypoidMeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshedGears, constructor.new(_910.KlingelnbergCycloPalloidHypoidMeshedGearDesign))
        return value
