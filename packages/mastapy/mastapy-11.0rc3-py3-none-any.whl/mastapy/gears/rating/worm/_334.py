﻿'''_334.py

WormGearMeshRating
'''


from typing import List

from mastapy.gears.gear_designs.worm import _888
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _335
from mastapy.gears.rating import _321
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Worm', 'WormGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshRating',)


class WormGearMeshRating(_321.GearMeshRating):
    '''WormGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def worm_gear_mesh(self) -> '_888.WormGearMeshDesign':
        '''WormGearMeshDesign: 'WormGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_888.WormGearMeshDesign)(self.wrapped.WormGearMesh) if self.wrapped.WormGearMesh else None

    @property
    def worm_gear_ratings(self) -> 'List[_335.WormGearRating]':
        '''List[WormGearRating]: 'WormGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearRatings, constructor.new(_335.WormGearRating))
        return value
