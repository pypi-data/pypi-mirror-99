﻿'''_1804.py

TaperRollerBearing
'''


from mastapy.bearings import _1542
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_designs.rolling import _1798, _1795
from mastapy._internal.python_net import python_net_import

_TAPER_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'TaperRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('TaperRollerBearing',)


class TaperRollerBearing(_1795.NonBarrelRollerBearing):
    '''TaperRollerBearing

    This is a mastapy class.
    '''

    TYPE = _TAPER_ROLLER_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TaperRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bearing_measurement_type(self) -> '_1542.BearingMeasurementType':
        '''BearingMeasurementType: 'BearingMeasurementType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BearingMeasurementType)
        return constructor.new(_1542.BearingMeasurementType)(value) if value else None

    @bearing_measurement_type.setter
    def bearing_measurement_type(self, value: '_1542.BearingMeasurementType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingMeasurementType = value

    @property
    def element_taper_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementTaperAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementTaperAngle) if self.wrapped.ElementTaperAngle else None

    @element_taper_angle.setter
    def element_taper_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ElementTaperAngle = value

    @property
    def cup_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CupAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CupAngle) if self.wrapped.CupAngle else None

    @cup_angle.setter
    def cup_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.CupAngle = value

    @property
    def cone_angle(self) -> 'float':
        '''float: 'ConeAngle' is the original name of this property.'''

        return self.wrapped.ConeAngle

    @cone_angle.setter
    def cone_angle(self, value: 'float'):
        self.wrapped.ConeAngle = float(value) if value else 0.0

    @property
    def mean_inner_race_diameter(self) -> 'float':
        '''float: 'MeanInnerRaceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanInnerRaceDiameter

    @property
    def mean_outer_race_diameter(self) -> 'float':
        '''float: 'MeanOuterRaceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanOuterRaceDiameter

    @property
    def width_setting_inner_and_outer_ring_width(self) -> 'float':
        '''float: 'WidthSettingInnerAndOuterRingWidth' is the original name of this property.'''

        return self.wrapped.WidthSettingInnerAndOuterRingWidth

    @width_setting_inner_and_outer_ring_width.setter
    def width_setting_inner_and_outer_ring_width(self, value: 'float'):
        self.wrapped.WidthSettingInnerAndOuterRingWidth = float(value) if value else 0.0

    @property
    def assembled_width(self) -> 'float':
        '''float: 'AssembledWidth' is the original name of this property.'''

        return self.wrapped.AssembledWidth

    @assembled_width.setter
    def assembled_width(self, value: 'float'):
        self.wrapped.AssembledWidth = float(value) if value else 0.0

    @property
    def width(self) -> 'float':
        '''float: 'Width' is the original name of this property.'''

        return self.wrapped.Width

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0

    @property
    def effective_centre_from_front_face(self) -> 'float':
        '''float: 'EffectiveCentreFromFrontFace' is the original name of this property.'''

        return self.wrapped.EffectiveCentreFromFrontFace

    @effective_centre_from_front_face.setter
    def effective_centre_from_front_face(self, value: 'float'):
        self.wrapped.EffectiveCentreFromFrontFace = float(value) if value else 0.0

    @property
    def effective_centre_to_front_face_set_by_changing_outer_ring_offset(self) -> 'float':
        '''float: 'EffectiveCentreToFrontFaceSetByChangingOuterRingOffset' is the original name of this property.'''

        return self.wrapped.EffectiveCentreToFrontFaceSetByChangingOuterRingOffset

    @effective_centre_to_front_face_set_by_changing_outer_ring_offset.setter
    def effective_centre_to_front_face_set_by_changing_outer_ring_offset(self, value: 'float'):
        self.wrapped.EffectiveCentreToFrontFaceSetByChangingOuterRingOffset = float(value) if value else 0.0

    @property
    def major_rib_detail(self) -> '_1798.RollerRibDetail':
        '''RollerRibDetail: 'MajorRibDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.RollerRibDetail)(self.wrapped.MajorRibDetail) if self.wrapped.MajorRibDetail else None
