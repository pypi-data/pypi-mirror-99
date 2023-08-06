﻿'''_488.py

ConicalGearRating
'''


from mastapy.gears.rating import _320, _322
from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical import _414, _415
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearRating',)


class ConicalGearRating(_322.GearRating):
    '''ConicalGearRating

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def concave_flank_rating(self) -> '_320.GearFlankRating':
        '''GearFlankRating: 'ConcaveFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _320.GearFlankRating.TYPE not in self.wrapped.ConcaveFlankRating.__class__.__mro__:
            raise CastException('Failed to cast concave_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.ConcaveFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConcaveFlankRating.__class__)(self.wrapped.ConcaveFlankRating) if self.wrapped.ConcaveFlankRating else None

    @property
    def convex_flank_rating(self) -> '_320.GearFlankRating':
        '''GearFlankRating: 'ConvexFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _320.GearFlankRating.TYPE not in self.wrapped.ConvexFlankRating.__class__.__mro__:
            raise CastException('Failed to cast convex_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.ConvexFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConvexFlankRating.__class__)(self.wrapped.ConvexFlankRating) if self.wrapped.ConvexFlankRating else None
