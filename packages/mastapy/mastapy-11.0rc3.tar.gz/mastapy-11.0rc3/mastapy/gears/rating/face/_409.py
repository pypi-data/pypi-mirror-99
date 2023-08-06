﻿'''_409.py

FaceGearRating
'''


from mastapy.gears.gear_designs.face import _919, _924, _927
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating import _322
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearRating',)


class FaceGearRating(_322.GearRating):
    '''FaceGearRating

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_gear(self) -> '_919.FaceGearDesign':
        '''FaceGearDesign: 'FaceGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.FaceGearDesign.TYPE not in self.wrapped.FaceGear.__class__.__mro__:
            raise CastException('Failed to cast face_gear to FaceGearDesign. Expected: {}.'.format(self.wrapped.FaceGear.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FaceGear.__class__)(self.wrapped.FaceGear) if self.wrapped.FaceGear else None
