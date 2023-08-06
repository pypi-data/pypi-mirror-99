﻿'''_2126.py

FaceGear
'''


from mastapy.system_model.part_model.gears import _2129, _2128
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.face import _754, _759, _762
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGear',)


class FaceGear(_2128.Gear):
    '''FaceGear

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def orientation(self) -> '_2129.GearOrientations':
        '''GearOrientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_2129.GearOrientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_2129.GearOrientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def active_gear_design(self) -> '_754.FaceGearDesign':
        '''FaceGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _754.FaceGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to FaceGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearDesign.__class__)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def face_gear_design(self) -> '_754.FaceGearDesign':
        '''FaceGearDesign: 'FaceGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _754.FaceGearDesign.TYPE not in self.wrapped.FaceGearDesign.__class__.__mro__:
            raise CastException('Failed to cast face_gear_design to FaceGearDesign. Expected: {}.'.format(self.wrapped.FaceGearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.FaceGearDesign.__class__)(self.wrapped.FaceGearDesign) if self.wrapped.FaceGearDesign else None
