﻿'''_365.py

SpiralBevelGearSetRating
'''


from typing import List

from mastapy.gears.gear_designs.spiral_bevel import _901
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.spiral_bevel import _363, _364
from mastapy.gears.rating.bevel import _504
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.SpiralBevel', 'SpiralBevelGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetRating',)


class SpiralBevelGearSetRating(_504.BevelGearSetRating):
    '''SpiralBevelGearSetRating

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def spiral_bevel_gear_set(self) -> '_901.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SpiralBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_901.SpiralBevelGearSetDesign)(self.wrapped.SpiralBevelGearSet) if self.wrapped.SpiralBevelGearSet else None

    @property
    def spiral_bevel_mesh_ratings(self) -> 'List[_363.SpiralBevelGearMeshRating]':
        '''List[SpiralBevelGearMeshRating]: 'SpiralBevelMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshRatings, constructor.new(_363.SpiralBevelGearMeshRating))
        return value

    @property
    def spiral_bevel_gear_ratings(self) -> 'List[_364.SpiralBevelGearRating]':
        '''List[SpiralBevelGearRating]: 'SpiralBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearRatings, constructor.new(_364.SpiralBevelGearRating))
        return value
