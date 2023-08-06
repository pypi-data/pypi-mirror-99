﻿'''_2244.py

ShaftHubConnection
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model.couplings import (
    _2238, _2241, _2237, _2240,
    _2231, _2239
)
from mastapy.detailed_rigid_connectors.splines import (
    _1173, _1158, _1178, _1153,
    _1156, _1160, _1163, _1164,
    _1171, _1183
)
from mastapy.scripting import _7157
from mastapy._internal.python_net import python_net_import
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.interference_fits import _1208
from mastapy.detailed_rigid_connectors.keyed_joints import _1200
from mastapy.nodal_analysis import _52
from mastapy.system_model.part_model import _2096

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_ARRAY = python_net_import('System', 'Array')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnection',)


class ShaftHubConnection(_2096.Connector):
    '''ShaftHubConnection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def radial_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialClearance) if self.wrapped.RadialClearance else None

    @radial_clearance.setter
    def radial_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RadialClearance = value

    @property
    def tilt_clearance(self) -> 'float':
        '''float: 'TiltClearance' is the original name of this property.'''

        return self.wrapped.TiltClearance

    @tilt_clearance.setter
    def tilt_clearance(self, value: 'float'):
        self.wrapped.TiltClearance = float(value) if value else 0.0

    @property
    def torsional_stiffness_shaft_hub_connection(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TorsionalStiffnessShaftHubConnection' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TorsionalStiffnessShaftHubConnection) if self.wrapped.TorsionalStiffnessShaftHubConnection else None

    @torsional_stiffness_shaft_hub_connection.setter
    def torsional_stiffness_shaft_hub_connection(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.TorsionalStiffnessShaftHubConnection = value

    @property
    def radial_stiffness_shaft_hub_connection(self) -> 'float':
        '''float: 'RadialStiffnessShaftHubConnection' is the original name of this property.'''

        return self.wrapped.RadialStiffnessShaftHubConnection

    @radial_stiffness_shaft_hub_connection.setter
    def radial_stiffness_shaft_hub_connection(self, value: 'float'):
        self.wrapped.RadialStiffnessShaftHubConnection = float(value) if value else 0.0

    @property
    def axial_stiffness_shaft_hub_connection(self) -> 'float':
        '''float: 'AxialStiffnessShaftHubConnection' is the original name of this property.'''

        return self.wrapped.AxialStiffnessShaftHubConnection

    @axial_stiffness_shaft_hub_connection.setter
    def axial_stiffness_shaft_hub_connection(self, value: 'float'):
        self.wrapped.AxialStiffnessShaftHubConnection = float(value) if value else 0.0

    @property
    def additional_tilt_stiffness(self) -> 'float':
        '''float: 'AdditionalTiltStiffness' is the original name of this property.'''

        return self.wrapped.AdditionalTiltStiffness

    @additional_tilt_stiffness.setter
    def additional_tilt_stiffness(self, value: 'float'):
        self.wrapped.AdditionalTiltStiffness = float(value) if value else 0.0

    @property
    def tilt_stiffness_shaft_hub_connection(self) -> 'float':
        '''float: 'TiltStiffnessShaftHubConnection' is the original name of this property.'''

        return self.wrapped.TiltStiffnessShaftHubConnection

    @tilt_stiffness_shaft_hub_connection.setter
    def tilt_stiffness_shaft_hub_connection(self, value: 'float'):
        self.wrapped.TiltStiffnessShaftHubConnection = float(value) if value else 0.0

    @property
    def outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterDiameter) if self.wrapped.OuterDiameter else None

    @outer_diameter.setter
    def outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.OuterDiameter = value

    @property
    def inner_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerDiameter) if self.wrapped.InnerDiameter else None

    @inner_diameter.setter
    def inner_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.InnerDiameter = value

    @property
    def tilt_stiffness_type(self) -> '_2238.RigidConnectorTiltStiffnessTypes':
        '''RigidConnectorTiltStiffnessTypes: 'TiltStiffnessType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TiltStiffnessType)
        return constructor.new(_2238.RigidConnectorTiltStiffnessTypes)(value) if value else None

    @tilt_stiffness_type.setter
    def tilt_stiffness_type(self, value: '_2238.RigidConnectorTiltStiffnessTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TiltStiffnessType = value

    @property
    def type_(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes':
        '''enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes: 'Type' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.Type, value) if self.wrapped.Type else None

    @type_.setter
    def type_(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Type = value

    @property
    def spline_type(self) -> '_1173.SplineDesignTypes':
        '''SplineDesignTypes: 'SplineType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SplineType)
        return constructor.new(_1173.SplineDesignTypes)(value) if value else None

    @spline_type.setter
    def spline_type(self, value: '_1173.SplineDesignTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SplineType = value

    @property
    def torsional_twist_preload(self) -> 'float':
        '''float: 'TorsionalTwistPreload' is the original name of this property.'''

        return self.wrapped.TorsionalTwistPreload

    @torsional_twist_preload.setter
    def torsional_twist_preload(self, value: 'float'):
        self.wrapped.TorsionalTwistPreload = float(value) if value else 0.0

    @property
    def axial_preload(self) -> 'float':
        '''float: 'AxialPreload' is the original name of this property.'''

        return self.wrapped.AxialPreload

    @axial_preload.setter
    def axial_preload(self, value: 'float'):
        self.wrapped.AxialPreload = float(value) if value else 0.0

    @property
    def two_d_spline_drawing(self) -> '_7157.SMTBitmap':
        '''SMTBitmap: 'TwoDSplineDrawing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7157.SMTBitmap)(self.wrapped.TwoDSplineDrawing) if self.wrapped.TwoDSplineDrawing else None

    @property
    def inner_half_material(self) -> 'str':
        '''str: 'InnerHalfMaterial' is the original name of this property.'''

        return self.wrapped.InnerHalfMaterial.SelectedItemName

    @inner_half_material.setter
    def inner_half_material(self, value: 'str'):
        self.wrapped.InnerHalfMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def outer_half_material(self) -> 'str':
        '''str: 'OuterHalfMaterial' is the original name of this property.'''

        return self.wrapped.OuterHalfMaterial.SelectedItemName

    @outer_half_material.setter
    def outer_half_material(self, value: 'str'):
        self.wrapped.OuterHalfMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def stiffness_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType':
        '''enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType: 'StiffnessType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.StiffnessType, value) if self.wrapped.StiffnessType else None

    @stiffness_type.setter
    def stiffness_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.StiffnessType = value

    @property
    def contact_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ContactDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ContactDiameter) if self.wrapped.ContactDiameter else None

    @contact_diameter.setter
    def contact_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ContactDiameter = value

    @property
    def number_of_contacts_per_direction(self) -> 'int':
        '''int: 'NumberOfContactsPerDirection' is the original name of this property.'''

        return self.wrapped.NumberOfContactsPerDirection

    @number_of_contacts_per_direction.setter
    def number_of_contacts_per_direction(self, value: 'int'):
        self.wrapped.NumberOfContactsPerDirection = int(value) if value else 0

    @property
    def angular_extent_of_external_teeth(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AngularExtentOfExternalTeeth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AngularExtentOfExternalTeeth) if self.wrapped.AngularExtentOfExternalTeeth else None

    @angular_extent_of_external_teeth.setter
    def angular_extent_of_external_teeth(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AngularExtentOfExternalTeeth = value

    @property
    def centre_angle_of_first_external_tooth(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CentreAngleOfFirstExternalTooth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CentreAngleOfFirstExternalTooth) if self.wrapped.CentreAngleOfFirstExternalTooth else None

    @centre_angle_of_first_external_tooth.setter
    def centre_angle_of_first_external_tooth(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.CentreAngleOfFirstExternalTooth = value

    @property
    def flank_contact_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'FlankContactStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.FlankContactStiffness) if self.wrapped.FlankContactStiffness else None

    @flank_contact_stiffness.setter
    def flank_contact_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.FlankContactStiffness = value

    @property
    def major_diameter_contact_stiffness(self) -> 'float':
        '''float: 'MajorDiameterContactStiffness' is the original name of this property.'''

        return self.wrapped.MajorDiameterContactStiffness

    @major_diameter_contact_stiffness.setter
    def major_diameter_contact_stiffness(self, value: 'float'):
        self.wrapped.MajorDiameterContactStiffness = float(value) if value else 0.0

    @property
    def pressure_angle(self) -> 'float':
        '''float: 'PressureAngle' is the original name of this property.'''

        return self.wrapped.PressureAngle

    @pressure_angle.setter
    def pressure_angle(self, value: 'float'):
        self.wrapped.PressureAngle = float(value) if value else 0.0

    @property
    def normal_clearance(self) -> 'float':
        '''float: 'NormalClearance' is the original name of this property.'''

        return self.wrapped.NormalClearance

    @normal_clearance.setter
    def normal_clearance(self, value: 'float'):
        self.wrapped.NormalClearance = float(value) if value else 0.0

    @property
    def angular_backlash(self) -> 'float':
        '''float: 'AngularBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngularBacklash

    @property
    def helix_angle(self) -> 'float':
        '''float: 'HelixAngle' is the original name of this property.'''

        return self.wrapped.HelixAngle

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def left_flank_helix_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LeftFlankHelixAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LeftFlankHelixAngle) if self.wrapped.LeftFlankHelixAngle else None

    @left_flank_helix_angle.setter
    def left_flank_helix_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.LeftFlankHelixAngle = value

    @property
    def right_flank_helix_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RightFlankHelixAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RightFlankHelixAngle) if self.wrapped.RightFlankHelixAngle else None

    @right_flank_helix_angle.setter
    def right_flank_helix_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RightFlankHelixAngle = value

    @property
    def type_of_fit(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FitTypes':
        '''enum_with_selected_value.EnumWithSelectedValue_FitTypes: 'TypeOfFit' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_FitTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.TypeOfFit, value) if self.wrapped.TypeOfFit else None

    @type_of_fit.setter
    def type_of_fit(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FitTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FitTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.TypeOfFit = value

    @property
    def tooth_spacing_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType':
        '''enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType: 'ToothSpacingType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ToothSpacingType, value) if self.wrapped.ToothSpacingType else None

    @tooth_spacing_type.setter
    def tooth_spacing_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ToothSpacingType = value

    @property
    def coefficient_of_friction(self) -> 'float':
        '''float: 'CoefficientOfFriction' is the original name of this property.'''

        return self.wrapped.CoefficientOfFriction

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'float'):
        self.wrapped.CoefficientOfFriction = float(value) if value else 0.0

    @property
    def tangential_stiffness(self) -> 'float':
        '''float: 'TangentialStiffness' is the original name of this property.'''

        return self.wrapped.TangentialStiffness

    @tangential_stiffness.setter
    def tangential_stiffness(self, value: 'float'):
        self.wrapped.TangentialStiffness = float(value) if value else 0.0

    @property
    def spline_joint_design(self) -> '_1178.SplineJointDesign':
        '''SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1178.SplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_custom_spline_joint_design(self) -> '_1153.CustomSplineJointDesign':
        '''CustomSplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1153.CustomSplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to CustomSplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_din5480_spline_joint_design(self) -> '_1156.DIN5480SplineJointDesign':
        '''DIN5480SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1156.DIN5480SplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to DIN5480SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_gbt3478_spline_joint_design(self) -> '_1160.GBT3478SplineJointDesign':
        '''GBT3478SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1160.GBT3478SplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to GBT3478SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_iso4156_spline_joint_design(self) -> '_1163.ISO4156SplineJointDesign':
        '''ISO4156SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1163.ISO4156SplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to ISO4156SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_jisb1603_spline_joint_design(self) -> '_1164.JISB1603SplineJointDesign':
        '''JISB1603SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1164.JISB1603SplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to JISB1603SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_sae_spline_joint_design(self) -> '_1171.SAESplineJointDesign':
        '''SAESplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1171.SAESplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to SAESplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_standard_spline_joint_design(self) -> '_1183.StandardSplineJointDesign':
        '''StandardSplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1183.StandardSplineJointDesign.TYPE not in self.wrapped.SplineJointDesign.__class__.__mro__:
            raise CastException('Failed to cast spline_joint_design to StandardSplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SplineJointDesign.__class__)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def interference_fit_design(self) -> '_1208.InterferenceFitDesign':
        '''InterferenceFitDesign: 'InterferenceFitDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1208.InterferenceFitDesign.TYPE not in self.wrapped.InterferenceFitDesign.__class__.__mro__:
            raise CastException('Failed to cast interference_fit_design to InterferenceFitDesign. Expected: {}.'.format(self.wrapped.InterferenceFitDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.InterferenceFitDesign.__class__)(self.wrapped.InterferenceFitDesign) if self.wrapped.InterferenceFitDesign else None

    @property
    def nonlinear_stiffness(self) -> '_52.DiagonalNonlinearStiffness':
        '''DiagonalNonlinearStiffness: 'NonlinearStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_52.DiagonalNonlinearStiffness)(self.wrapped.NonlinearStiffness) if self.wrapped.NonlinearStiffness else None

    @property
    def flank_lead_crowning(self) -> '_2231.CrowningSpecification':
        '''CrowningSpecification: 'FlankLeadCrowning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2231.CrowningSpecification)(self.wrapped.FlankLeadCrowning) if self.wrapped.FlankLeadCrowning else None

    @property
    def tooth_locations_external_spline_half(self) -> 'List[_2239.RigidConnectorToothLocation]':
        '''List[RigidConnectorToothLocation]: 'ToothLocationsExternalSplineHalf' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ToothLocationsExternalSplineHalf, constructor.new(_2239.RigidConnectorToothLocation))
        return value

    @property
    def full_stiffness_matrix(self) -> 'List[List[float]]':
        '''List[List[float]]: 'FullStiffnessMatrix' is the original name of this property.'''

        value = conversion.pn_to_mp_list_float_2d(self.wrapped.FullStiffnessMatrix)
        return value

    @full_stiffness_matrix.setter
    def full_stiffness_matrix(self, value: 'List[List[float]]'):
        value = value if value else None
        value = conversion.mp_to_pn_list_float_2d(value)
        self.wrapped.FullStiffnessMatrix = value
