﻿'''_208.py

KlingelnbergCycloPalloidSpiralBevelGearRating
'''


from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _739
from mastapy._internal import constructor
from mastapy.gears.rating.klingelnberg_conical import _214
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergSpiralBevel', 'KlingelnbergCycloPalloidSpiralBevelGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearRating',)


class KlingelnbergCycloPalloidSpiralBevelGearRating(_214.KlingelnbergCycloPalloidConicalGearRating):
    '''KlingelnbergCycloPalloidSpiralBevelGearRating

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_739.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'KlingelnbergCycloPalloidSpiralBevelGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_739.KlingelnbergCycloPalloidSpiralBevelGearDesign)(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGear) if self.wrapped.KlingelnbergCycloPalloidSpiralBevelGear else None
