﻿'''_2062.py

FESubstructure
'''


from typing import List, Optional

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable, list_with_selected_item, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility.units_and_measurements import _1365
from mastapy.system_model.fe import (
    _2042, _2065, _2088, _2036,
    _2038, _2063, _2086, _2064,
    _2060, _2072, _2073, _2071,
    _2068, _2069, _2070
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.part_model import _2126, _2122, _2130
from mastapy.nodal_analysis import _64, _55, _60
from mastapy.nodal_analysis.component_mode_synthesis import _196
from mastapy.nodal_analysis.space_claim_link import _119
from mastapy.system_model import _1904
from mastapy.math_utility import _1261
from mastapy.materials import _205, _247
from mastapy.system_model.part_model.shaft_model import _2158
from mastapy.system_model.fe.links import _2095
from mastapy.math_utility.measured_vectors import _1326
from mastapy import _7196
from mastapy.nodal_analysis.fe_export_utility import _149

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_STRING = python_net_import('System', 'String')
_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_FE_SUBSTRUCTURE = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructure')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructure',)


class FESubstructure(_60.FEStiffness):
    '''FESubstructure

    This is a mastapy class.
    '''

    TYPE = _FE_SUBSTRUCTURE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FESubstructure.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def external_fe_forces_are_from_gravity_only(self) -> 'bool':
        '''bool: 'ExternalFEForcesAreFromGravityOnly' is the original name of this property.'''

        return self.wrapped.ExternalFEForcesAreFromGravityOnly

    @external_fe_forces_are_from_gravity_only.setter
    def external_fe_forces_are_from_gravity_only(self, value: 'bool'):
        self.wrapped.ExternalFEForcesAreFromGravityOnly = bool(value) if value else False

    @property
    def housing_is_grounded(self) -> 'bool':
        '''bool: 'HousingIsGrounded' is the original name of this property.'''

        return self.wrapped.HousingIsGrounded

    @housing_is_grounded.setter
    def housing_is_grounded(self, value: 'bool'):
        self.wrapped.HousingIsGrounded = bool(value) if value else False

    @property
    def check_fe_has_internal_modes_before_nvh_analysis(self) -> 'bool':
        '''bool: 'CheckFEHasInternalModesBeforeNVHAnalysis' is the original name of this property.'''

        return self.wrapped.CheckFEHasInternalModesBeforeNVHAnalysis

    @check_fe_has_internal_modes_before_nvh_analysis.setter
    def check_fe_has_internal_modes_before_nvh_analysis(self, value: 'bool'):
        self.wrapped.CheckFEHasInternalModesBeforeNVHAnalysis = bool(value) if value else False

    @property
    def expected_number_of_rigid_body_modes(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'ExpectedNumberOfRigidBodyModes' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.ExpectedNumberOfRigidBodyModes) if self.wrapped.ExpectedNumberOfRigidBodyModes else None

    @expected_number_of_rigid_body_modes.setter
    def expected_number_of_rigid_body_modes(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.ExpectedNumberOfRigidBodyModes = value

    @property
    def actual_number_of_rigid_body_modes(self) -> 'int':
        '''int: 'ActualNumberOfRigidBodyModes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ActualNumberOfRigidBodyModes

    @property
    def is_housing(self) -> 'bool':
        '''bool: 'IsHousing' is the original name of this property.'''

        return self.wrapped.IsHousing

    @is_housing.setter
    def is_housing(self, value: 'bool'):
        self.wrapped.IsHousing = bool(value) if value else False

    @property
    def distance_display_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'DistanceDisplayUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.DistanceDisplayUnit) if self.wrapped.DistanceDisplayUnit else None

    @distance_display_unit.setter
    def distance_display_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.DistanceDisplayUnit = value

    @property
    def force_display_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'ForceDisplayUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.ForceDisplayUnit) if self.wrapped.ForceDisplayUnit else None

    @force_display_unit.setter
    def force_display_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ForceDisplayUnit = value

    @property
    def non_condensation_node_size(self) -> 'int':
        '''int: 'NonCondensationNodeSize' is the original name of this property.'''

        return self.wrapped.NonCondensationNodeSize

    @non_condensation_node_size.setter
    def non_condensation_node_size(self, value: 'int'):
        self.wrapped.NonCondensationNodeSize = int(value) if value else 0

    @property
    def angular_alignment_tolerance(self) -> 'float':
        '''float: 'AngularAlignmentTolerance' is the original name of this property.'''

        return self.wrapped.AngularAlignmentTolerance

    @angular_alignment_tolerance.setter
    def angular_alignment_tolerance(self, value: 'float'):
        self.wrapped.AngularAlignmentTolerance = float(value) if value else 0.0

    @property
    def bearing_node_alignment(self) -> '_2042.BearingNodeAlignmentOption':
        '''BearingNodeAlignmentOption: 'BearingNodeAlignment' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BearingNodeAlignment)
        return constructor.new(_2042.BearingNodeAlignmentOption)(value) if value else None

    @bearing_node_alignment.setter
    def bearing_node_alignment(self, value: '_2042.BearingNodeAlignmentOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingNodeAlignment = value

    @property
    def comment(self) -> 'str':
        '''str: 'Comment' is the original name of this property.'''

        return self.wrapped.Comment

    @comment.setter
    def comment(self, value: 'str'):
        self.wrapped.Comment = str(value) if value else None

    @property
    def polar_inertia(self) -> 'float':
        '''float: 'PolarInertia' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PolarInertia

    @property
    def torque_transmission_relative_tolerance(self) -> 'float':
        '''float: 'TorqueTransmissionRelativeTolerance' is the original name of this property.'''

        return self.wrapped.TorqueTransmissionRelativeTolerance

    @torque_transmission_relative_tolerance.setter
    def torque_transmission_relative_tolerance(self, value: 'float'):
        self.wrapped.TorqueTransmissionRelativeTolerance = float(value) if value else 0.0

    @property
    def type_(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FESubstructureType':
        '''enum_with_selected_value.EnumWithSelectedValue_FESubstructureType: 'Type' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.Type, value) if self.wrapped.Type else None

    @type_.setter
    def type_(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Type = value

    @property
    def full_fe_model_mesh_path(self) -> 'str':
        '''str: 'FullFEModelMeshPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FullFEModelMeshPath

    @property
    def full_fe_model_vectors_path(self) -> 'str':
        '''str: 'FullFEModelVectorsPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FullFEModelVectorsPath

    @property
    def material(self) -> 'str':
        '''str: 'Material' is the original name of this property.'''

        return self.wrapped.Material.SelectedItemName

    @material.setter
    def material(self, value: 'str'):
        self.wrapped.Material.SetSelectedItem(str(value) if value else None)

    @property
    def thermal_expansion_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption: 'ThermalExpansionOption' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ThermalExpansionOption, value) if self.wrapped.ThermalExpansionOption else None

    @thermal_expansion_option.setter
    def thermal_expansion_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ThermalExpansionOption = value

    @property
    def number_of_condensation_nodes_in_reduced_model(self) -> 'int':
        '''int: 'NumberOfCondensationNodesInReducedModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfCondensationNodesInReducedModel

    @property
    def number_of_condensation_nodes(self) -> 'int':
        '''int: 'NumberOfCondensationNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfCondensationNodes

    @property
    def datum(self) -> 'list_with_selected_item.ListWithSelectedItem_Datum':
        '''list_with_selected_item.ListWithSelectedItem_Datum: 'Datum' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Datum)(self.wrapped.Datum) if self.wrapped.Datum else None

    @datum.setter
    def datum(self, value: 'list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Datum.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Datum = value

    @property
    def alignment_method(self) -> '_2036.AlignmentMethod':
        '''AlignmentMethod: 'AlignmentMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AlignmentMethod)
        return constructor.new(_2036.AlignmentMethod)(value) if value else None

    @alignment_method.setter
    def alignment_method(self, value: '_2036.AlignmentMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AlignmentMethod = value

    @property
    def component_to_align_to(self) -> 'list_with_selected_item.ListWithSelectedItem_Component':
        '''list_with_selected_item.ListWithSelectedItem_Component: 'ComponentToAlignTo' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Component)(self.wrapped.ComponentToAlignTo) if self.wrapped.ComponentToAlignTo else None

    @component_to_align_to.setter
    def component_to_align_to(self, value: 'list_with_selected_item.ListWithSelectedItem_Component.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Component.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Component.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ComponentToAlignTo = value

    @property
    def apply_translation_and_rotation_for_planetary_duplicates(self) -> 'bool':
        '''bool: 'ApplyTranslationAndRotationForPlanetaryDuplicates' is the original name of this property.'''

        return self.wrapped.ApplyTranslationAndRotationForPlanetaryDuplicates

    @apply_translation_and_rotation_for_planetary_duplicates.setter
    def apply_translation_and_rotation_for_planetary_duplicates(self, value: 'bool'):
        self.wrapped.ApplyTranslationAndRotationForPlanetaryDuplicates = bool(value) if value else False

    @property
    def full_fe_model_mesh_size(self) -> 'str':
        '''str: 'FullFEModelMeshSize' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FullFEModelMeshSize

    @property
    def full_fe_model_vectors_size(self) -> 'str':
        '''str: 'FullFEModelVectorsSize' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FullFEModelVectorsSize

    @property
    def number_of_angles(self) -> 'int':
        '''int: 'NumberOfAngles' is the original name of this property.'''

        return self.wrapped.NumberOfAngles

    @number_of_angles.setter
    def number_of_angles(self, value: 'int'):
        self.wrapped.NumberOfAngles = int(value) if value else 0

    @property
    def angle_span(self) -> 'float':
        '''float: 'AngleSpan' is the original name of this property.'''

        return self.wrapped.AngleSpan

    @angle_span.setter
    def angle_span(self, value: 'float'):
        self.wrapped.AngleSpan = float(value) if value else 0.0

    @property
    def condensation_node_size(self) -> 'float':
        '''float: 'CondensationNodeSize' is the original name of this property.'''

        return self.wrapped.CondensationNodeSize

    @condensation_node_size.setter
    def condensation_node_size(self, value: 'float'):
        self.wrapped.CondensationNodeSize = float(value) if value else 0.0

    @property
    def bearing_races_in_fe(self) -> 'bool':
        '''bool: 'BearingRacesInFE' is the original name of this property.'''

        return self.wrapped.BearingRacesInFE

    @bearing_races_in_fe.setter
    def bearing_races_in_fe(self, value: 'bool'):
        self.wrapped.BearingRacesInFE = bool(value) if value else False

    @property
    def is_mesh_loaded(self) -> 'bool':
        '''bool: 'IsMeshLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsMeshLoaded

    @property
    def are_vectors_loaded(self) -> 'bool':
        '''bool: 'AreVectorsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AreVectorsLoaded

    @property
    def gravity_force_source(self) -> '_64.GravityForceSource':
        '''GravityForceSource: 'GravityForceSource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.GravityForceSource)
        return constructor.new(_64.GravityForceSource)(value) if value else None

    @property
    def gravity_force_can_be_rotated(self) -> 'bool':
        '''bool: 'GravityForceCanBeRotated' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GravityForceCanBeRotated

    @property
    def reduced_stiffness_file_editable(self) -> 'str':
        '''str: 'ReducedStiffnessFileEditable' is the original name of this property.'''

        return self.wrapped.ReducedStiffnessFileEditable

    @reduced_stiffness_file_editable.setter
    def reduced_stiffness_file_editable(self, value: 'str'):
        self.wrapped.ReducedStiffnessFileEditable = str(value) if value else None

    @property
    def reduced_stiffness_file(self) -> 'str':
        '''str: 'ReducedStiffnessFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReducedStiffnessFile

    @property
    def gravity_magnitude_used_for_reduced_forces(self) -> 'float':
        '''float: 'GravityMagnitudeUsedForReducedForces' is the original name of this property.'''

        return self.wrapped.GravityMagnitudeUsedForReducedForces

    @gravity_magnitude_used_for_reduced_forces.setter
    def gravity_magnitude_used_for_reduced_forces(self, value: 'float'):
        self.wrapped.GravityMagnitudeUsedForReducedForces = float(value) if value else 0.0

    @property
    def fe_meshing_options(self) -> '_55.FEMeshingOptions':
        '''FEMeshingOptions: 'FEMeshingOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_55.FEMeshingOptions)(self.wrapped.FEMeshingOptions) if self.wrapped.FEMeshingOptions else None

    @property
    def cms_model(self) -> '_196.CMSModel':
        '''CMSModel: 'CMSModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_196.CMSModel)(self.wrapped.CMSModel) if self.wrapped.CMSModel else None

    @property
    def space_claim_dimensions(self) -> '_119.SpaceClaimDimensions':
        '''SpaceClaimDimensions: 'SpaceClaimDimensions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_119.SpaceClaimDimensions)(self.wrapped.SpaceClaimDimensions) if self.wrapped.SpaceClaimDimensions else None

    @property
    def alignment_to_component(self) -> '_1904.RelativeComponentAlignment[_2122.Component]':
        '''RelativeComponentAlignment[Component]: 'AlignmentToComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.RelativeComponentAlignment)[_2122.Component](self.wrapped.AlignmentToComponent) if self.wrapped.AlignmentToComponent else None

    @property
    def alignment_using_axial_node_positions(self) -> '_2038.AlignmentUsingAxialNodePositions':
        '''AlignmentUsingAxialNodePositions: 'AlignmentUsingAxialNodePositions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2038.AlignmentUsingAxialNodePositions)(self.wrapped.AlignmentUsingAxialNodePositions) if self.wrapped.AlignmentUsingAxialNodePositions else None

    @property
    def coordinate_system(self) -> '_1261.CoordinateSystem3D':
        '''CoordinateSystem3D: 'CoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1261.CoordinateSystem3D)(self.wrapped.CoordinateSystem) if self.wrapped.CoordinateSystem else None

    @property
    def export(self) -> '_2063.FESubstructureExportOptions':
        '''FESubstructureExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2063.FESubstructureExportOptions)(self.wrapped.Export) if self.wrapped.Export else None

    @property
    def acoustic_radiation_efficiency(self) -> '_205.AcousticRadiationEfficiency':
        '''AcousticRadiationEfficiency: 'AcousticRadiationEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_205.AcousticRadiationEfficiency)(self.wrapped.AcousticRadiationEfficiency) if self.wrapped.AcousticRadiationEfficiency else None

    @property
    def sound_pressure_enclosure(self) -> '_247.SoundPressureEnclosure':
        '''SoundPressureEnclosure: 'SoundPressureEnclosure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_247.SoundPressureEnclosure)(self.wrapped.SoundPressureEnclosure) if self.wrapped.SoundPressureEnclosure else None

    @property
    def shafts_that_can_be_replaced(self) -> 'List[_2086.ReplacedShaftSelectionHelper]':
        '''List[ReplacedShaftSelectionHelper]: 'ShaftsThatCanBeReplaced' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsThatCanBeReplaced, constructor.new(_2086.ReplacedShaftSelectionHelper))
        return value

    @property
    def nodes(self) -> 'List[_2064.FESubstructureNode]':
        '''List[FESubstructureNode]: 'Nodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Nodes, constructor.new(_2064.FESubstructureNode))
        return value

    @property
    def replaced_shafts(self) -> 'List[_2158.Shaft]':
        '''List[Shaft]: 'ReplacedShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReplacedShafts, constructor.new(_2158.Shaft))
        return value

    @property
    def links(self) -> 'List[_2095.FELink]':
        '''List[FELink]: 'Links' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Links, constructor.new(_2095.FELink))
        return value

    @property
    def thermal_expansion_forces(self) -> 'List[_1326.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'ThermalExpansionForces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ThermalExpansionForces, constructor.new(_1326.VectorWithLinearAndAngularComponents))
        return value

    @property
    def thermal_expansion_displacements(self) -> 'List[_1326.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'ThermalExpansionDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ThermalExpansionDisplacements, constructor.new(_1326.VectorWithLinearAndAngularComponents))
        return value

    @property
    def geometries(self) -> 'List[_2060.FEStiffnessGeometry]':
        '''List[FEStiffnessGeometry]: 'Geometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Geometries, constructor.new(_2060.FEStiffnessGeometry))
        return value

    @property
    def gear_meshing_options(self) -> 'List[_2072.GearMeshingOptions]':
        '''List[GearMeshingOptions]: 'GearMeshingOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshingOptions, constructor.new(_2072.GearMeshingOptions))
        return value

    @property
    def independent_masta_created_condensation_nodes(self) -> 'List[_2073.IndependentMastaCreatedCondensationNode]':
        '''List[IndependentMastaCreatedCondensationNode]: 'IndependentMastaCreatedCondensationNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.IndependentMastaCreatedCondensationNodes, constructor.new(_2073.IndependentMastaCreatedCondensationNode))
        return value

    @property
    def fe_part(self) -> '_2130.FEPart':
        '''FEPart: 'FEPart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FEPart)(self.wrapped.FEPart) if self.wrapped.FEPart else None

    def auto_connect_external_nodes(self):
        ''' 'AutoConnectExternalNodes' is the original name of this method.'''

        self.wrapped.AutoConnectExternalNodes()

    def default_node_creation_options(self):
        ''' 'DefaultNodeCreationOptions' is the original name of this method.'''

        self.wrapped.DefaultNodeCreationOptions()

    def add_geometry(self):
        ''' 'AddGeometry' is the original name of this method.'''

        self.wrapped.AddGeometry()

    def import_node_positions(self):
        ''' 'ImportNodePositions' is the original name of this method.'''

        self.wrapped.ImportNodePositions()

    def read_stl_file(self):
        ''' 'ReadSTLFile' is the original name of this method.'''

        self.wrapped.ReadSTLFile()

    def reread_mesh_from_space_claim(self):
        ''' 'RereadMeshFromSpaceClaim' is the original name of this method.'''

        self.wrapped.RereadMeshFromSpaceClaim()

    def create_fe_volume_mesh(self):
        ''' 'CreateFEVolumeMesh' is the original name of this method.'''

        self.wrapped.CreateFEVolumeMesh()

    def update_gear_teeth_mesh(self):
        ''' 'UpdateGearTeethMesh' is the original name of this method.'''

        self.wrapped.UpdateGearTeethMesh()

    def open_existing_smtfe_file(self):
        ''' 'OpenExistingSMTFEFile' is the original name of this method.'''

        self.wrapped.OpenExistingSMTFEFile()

    def re_import_external_fe_mesh(self):
        ''' 'ReImportExternalFEMesh' is the original name of this method.'''

        self.wrapped.ReImportExternalFEMesh()

    def perform_reduction(self):
        ''' 'PerformReduction' is the original name of this method.'''

        self.wrapped.PerformReduction()

    def copy_datum_to_manual(self):
        ''' 'CopyDatumToManual' is the original name of this method.'''

        self.wrapped.CopyDatumToManual()

    def delete_all_links(self):
        ''' 'DeleteAllLinks' is the original name of this method.'''

        self.wrapped.DeleteAllLinks()

    def embed_fe_model_mesh_in_masta_file(self):
        ''' 'EmbedFEModelMeshInMASTAFile' is the original name of this method.'''

        self.wrapped.EmbedFEModelMeshInMASTAFile()

    def embed_fe_model_vectors_in_masta_file(self):
        ''' 'EmbedFEModelVectorsInMASTAFile' is the original name of this method.'''

        self.wrapped.EmbedFEModelVectorsInMASTAFile()

    def store_full_fe_model_mesh_in_external_file(self):
        ''' 'StoreFullFEModelMeshInExternalFile' is the original name of this method.'''

        self.wrapped.StoreFullFEModelMeshInExternalFile()

    def store_full_fe_model_vectors_in_external_file(self):
        ''' 'StoreFullFEModelVectorsInExternalFile' is the original name of this method.'''

        self.wrapped.StoreFullFEModelVectorsInExternalFile()

    def unload_external_mesh_file(self):
        ''' 'UnloadExternalMeshFile' is the original name of this method.'''

        self.wrapped.UnloadExternalMeshFile()

    def load_external_mesh_file(self):
        ''' 'LoadExternalMeshFile' is the original name of this method.'''

        self.wrapped.LoadExternalMeshFile()

    def unload_external_vectors_file(self):
        ''' 'UnloadExternalVectorsFile' is the original name of this method.'''

        self.wrapped.UnloadExternalVectorsFile()

    def load_external_vectors_file(self):
        ''' 'LoadExternalVectorsFile' is the original name of this method.'''

        self.wrapped.LoadExternalVectorsFile()

    def remove_full_fe_mesh(self):
        ''' 'RemoveFullFEMesh' is the original name of this method.'''

        self.wrapped.RemoveFullFEMesh()

    def create_datum_from_manual_alignment(self):
        ''' 'CreateDatumFromManualAlignment' is the original name of this method.'''

        self.wrapped.CreateDatumFromManualAlignment()

    def load_existing_masta_fe_file(self, file_name: 'str'):
        ''' 'LoadExistingMastaFEFile' is the original name of this method.

        Args:
            file_name (str)
        '''

        file_name = str(file_name)
        self.wrapped.LoadExistingMastaFEFile.Overloads[_STRING](file_name if file_name else None)

    def load_existing_masta_fe_file_with_progress(self, file_name: 'str', progress: '_7196.TaskProgress'):
        ''' 'LoadExistingMastaFEFile' is the original name of this method.

        Args:
            file_name (str)
            progress (mastapy.TaskProgress)
        '''

        file_name = str(file_name)
        self.wrapped.LoadExistingMastaFEFile.Overloads[_STRING, _TASK_PROGRESS](file_name if file_name else None, progress.wrapped if progress else None)

    def create_fe_substructure_with_selection_for_static_analysis(self) -> '_2071.FESubstructureWithSelectionForStaticAnalysis':
        ''' 'CreateFESubstructureWithSelectionForStaticAnalysis' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionForStaticAnalysis
        '''

        method_result = self.wrapped.CreateFESubstructureWithSelectionForStaticAnalysis()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def create_fe_substructure_with_selection_components(self) -> '_2068.FESubstructureWithSelectionComponents':
        ''' 'CreateFESubstructureWithSelectionComponents' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionComponents
        '''

        method_result = self.wrapped.CreateFESubstructureWithSelectionComponents()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def create_fe_substructure_with_selection_for_harmonic_analysis(self) -> '_2069.FESubstructureWithSelectionForHarmonicAnalysis':
        ''' 'CreateFESubstructureWithSelectionForHarmonicAnalysis' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionForHarmonicAnalysis
        '''

        method_result = self.wrapped.CreateFESubstructureWithSelectionForHarmonicAnalysis()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def create_fe_substructure_with_selection_for_modal_analysis(self) -> '_2070.FESubstructureWithSelectionForModalAnalysis':
        ''' 'CreateFESubstructureWithSelectionForModalAnalysis' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionForModalAnalysis
        '''

        method_result = self.wrapped.CreateFESubstructureWithSelectionForModalAnalysis()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def import_fe_mesh(self, file_path: 'str', format_: '_149.FEExportFormat', length_scale: Optional['float'] = 1.0, force_scale: Optional['float'] = 1.0, progress: Optional['_7196.TaskProgress'] = None):
        ''' 'ImportFEMesh' is the original name of this method.

        Args:
            file_path (str)
            format_ (mastapy.nodal_analysis.fe_export_utility.FEExportFormat)
            length_scale (float, optional)
            force_scale (float, optional)
            progress (mastapy.TaskProgress, optional)
        '''

        file_path = str(file_path)
        format_ = conversion.mp_to_pn_enum(format_)
        length_scale = float(length_scale)
        force_scale = float(force_scale)
        self.wrapped.ImportFEMesh(file_path if file_path else None, format_, length_scale if length_scale else 0.0, force_scale if force_scale else 0.0, progress.wrapped if progress else None)

    def store_full_fe_mesh_in_external_file(self, external_fe_path: 'str'):
        ''' 'StoreFullFeMeshInExternalFile' is the original name of this method.

        Args:
            external_fe_path (str)
        '''

        external_fe_path = str(external_fe_path)
        self.wrapped.StoreFullFeMeshInExternalFile(external_fe_path if external_fe_path else None)

    def links_for(self, node: '_2064.FESubstructureNode') -> 'List[_2095.FELink]':
        ''' 'LinksFor' is the original name of this method.

        Args:
            node (mastapy.system_model.fe.FESubstructureNode)

        Returns:
            List[mastapy.system_model.fe.links.FELink]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.LinksFor(node.wrapped if node else None), constructor.new(_2095.FELink))
