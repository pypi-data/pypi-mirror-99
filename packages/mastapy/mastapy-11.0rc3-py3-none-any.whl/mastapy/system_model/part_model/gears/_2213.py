﻿'''_2213.py

KlingelnbergCycloPalloidHypoidGear
'''


from mastapy.gears.gear_designs.klingelnberg_hypoid import _907
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2211
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGear',)


class KlingelnbergCycloPalloidHypoidGear(_2211.KlingelnbergCycloPalloidConicalGear):
    '''KlingelnbergCycloPalloidHypoidGear

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_gear_design(self) -> '_907.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_907.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_907.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'KlingelnbergCycloPalloidHypoidGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_907.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.KlingelnbergCycloPalloidHypoidGearDesign) if self.wrapped.KlingelnbergCycloPalloidHypoidGearDesign else None
