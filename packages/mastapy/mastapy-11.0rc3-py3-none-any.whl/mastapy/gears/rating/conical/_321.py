﻿'''_321.py

ConicalGearDutyCycleRating
'''


from typing import List

from mastapy.gears.rating.conical import _324, _323
from mastapy._internal import constructor, conversion
from mastapy.gears.rating import _158, _157
from mastapy.gears.rating.cylindrical import _252, _253
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalGearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearDutyCycleRating',)


class ConicalGearDutyCycleRating(_157.GearDutyCycleRating):
    '''ConicalGearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_design_duty_cycle(self) -> '_324.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_324.ConicalGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def conical_gear_set_design_duty_cycle(self) -> '_324.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'ConicalGearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_324.ConicalGearSetDutyCycleRating)(self.wrapped.ConicalGearSetDesignDutyCycle) if self.wrapped.ConicalGearSetDesignDutyCycle else None

    @property
    def left_flank_rating(self) -> '_158.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _158.GearFlankRating.TYPE not in self.wrapped.LeftFlankRating.__class__.__mro__:
            raise CastException('Failed to cast left_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.LeftFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LeftFlankRating.__class__)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def concave_flank_rating(self) -> '_158.GearFlankRating':
        '''GearFlankRating: 'ConcaveFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _158.GearFlankRating.TYPE not in self.wrapped.ConcaveFlankRating.__class__.__mro__:
            raise CastException('Failed to cast concave_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.ConcaveFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConcaveFlankRating.__class__)(self.wrapped.ConcaveFlankRating) if self.wrapped.ConcaveFlankRating else None

    @property
    def right_flank_rating(self) -> '_158.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _158.GearFlankRating.TYPE not in self.wrapped.RightFlankRating.__class__.__mro__:
            raise CastException('Failed to cast right_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.RightFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RightFlankRating.__class__)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None

    @property
    def convex_flank_rating(self) -> '_158.GearFlankRating':
        '''GearFlankRating: 'ConvexFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _158.GearFlankRating.TYPE not in self.wrapped.ConvexFlankRating.__class__.__mro__:
            raise CastException('Failed to cast convex_flank_rating to GearFlankRating. Expected: {}.'.format(self.wrapped.ConvexFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConvexFlankRating.__class__)(self.wrapped.ConvexFlankRating) if self.wrapped.ConvexFlankRating else None

    @property
    def gear_ratings(self) -> 'List[_323.ConicalGearRating]':
        '''List[ConicalGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_323.ConicalGearRating))
        return value

    @property
    def conical_gear_ratings(self) -> 'List[_323.ConicalGearRating]':
        '''List[ConicalGearRating]: 'ConicalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGearRatings, constructor.new(_323.ConicalGearRating))
        return value
