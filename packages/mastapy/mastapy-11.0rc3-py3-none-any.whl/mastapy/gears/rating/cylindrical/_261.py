﻿'''_261.py

CylindricalGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical import _258, _254, _256
from mastapy.gears.rating.cylindrical.optimisation import _292
from mastapy.gears.gear_designs.cylindrical import _786, _795
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical.vdi import _280
from mastapy.gears.rating import _162
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetRating',)


class CylindricalGearSetRating(_162.GearSetRating):
    '''CylindricalGearSetRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating_standard_name(self) -> 'str':
        '''str: 'RatingStandardName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RatingStandardName

    @property
    def rating_settings(self) -> '_258.CylindricalGearRatingSettings':
        '''CylindricalGearRatingSettings: 'RatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_258.CylindricalGearRatingSettings)(self.wrapped.RatingSettings) if self.wrapped.RatingSettings else None

    @property
    def optimisations(self) -> '_292.CylindricalGearSetRatingOptimisationHelper':
        '''CylindricalGearSetRatingOptimisationHelper: 'Optimisations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_292.CylindricalGearSetRatingOptimisationHelper)(self.wrapped.Optimisations) if self.wrapped.Optimisations else None

    @property
    def cylindrical_gear_set(self) -> '_786.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'CylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _786.CylindricalGearSetDesign.TYPE not in self.wrapped.CylindricalGearSet.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_set to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.CylindricalGearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSet.__class__)(self.wrapped.CylindricalGearSet) if self.wrapped.CylindricalGearSet else None

    @property
    def vdi_cylindrical_gear_single_flank_ratings(self) -> 'List[_280.VDI2737InternalGearSingleFlankRating]':
        '''List[VDI2737InternalGearSingleFlankRating]: 'VDICylindricalGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.VDICylindricalGearSingleFlankRatings, constructor.new(_280.VDI2737InternalGearSingleFlankRating))
        return value

    @property
    def cylindrical_mesh_ratings(self) -> 'List[_254.CylindricalGearMeshRating]':
        '''List[CylindricalGearMeshRating]: 'CylindricalMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshRatings, constructor.new(_254.CylindricalGearMeshRating))
        return value

    @property
    def gear_ratings(self) -> 'List[_256.CylindricalGearRating]':
        '''List[CylindricalGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_256.CylindricalGearRating))
        return value

    @property
    def cylindrical_gear_ratings(self) -> 'List[_256.CylindricalGearRating]':
        '''List[CylindricalGearRating]: 'CylindricalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearRatings, constructor.new(_256.CylindricalGearRating))
        return value
