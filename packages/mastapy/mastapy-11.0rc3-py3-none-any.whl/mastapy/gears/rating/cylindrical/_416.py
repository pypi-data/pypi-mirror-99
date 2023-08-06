﻿'''_416.py

CylindricalGearMeshRating
'''


from typing import List

from mastapy.gears import _284, _302
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.rating.cylindrical import _426, _423, _418
from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _446, _448, _450
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical.iso6336 import (
    _467, _469, _471, _473,
    _475
)
from mastapy.gears.rating.cylindrical.din3990 import _482
from mastapy.gears.rating.cylindrical.agma import _484
from mastapy.gears.load_case.cylindrical import _820
from mastapy.gears.rating.cylindrical.vdi import _445
from mastapy.gears.gear_designs.cylindrical import _949
from mastapy.gears.rating import _321
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshRating',)


class CylindricalGearMeshRating(_321.GearMeshRating):
    '''CylindricalGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_284.CylindricalFlanks':
        '''CylindricalFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ActiveFlank)
        return constructor.new(_284.CylindricalFlanks)(value) if value else None

    @property
    def sliding_ratio_at_start_of_approach(self) -> 'float':
        '''float: 'SlidingRatioAtStartOfApproach' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SlidingRatioAtStartOfApproach

    @property
    def sliding_ratio_at_end_of_recess(self) -> 'float':
        '''float: 'SlidingRatioAtEndOfRecess' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SlidingRatioAtEndOfRecess

    @property
    def mechanical_advantage(self) -> 'float':
        '''float: 'MechanicalAdvantage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MechanicalAdvantage

    @property
    def mesh_coefficient_of_friction(self) -> 'float':
        '''float: 'MeshCoefficientOfFriction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFriction

    @property
    def mesh_coefficient_of_friction_isotr1417912001(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionISOTR1417912001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionISOTR1417912001

    @property
    def mesh_coefficient_of_friction_isotr1417912001_with_surface_roughness_parameter(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionISOTR1417912001WithSurfaceRoughnessParameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionISOTR1417912001WithSurfaceRoughnessParameter

    @property
    def mesh_coefficient_of_friction_isotr1417922001(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionISOTR1417922001' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionISOTR1417922001

    @property
    def mesh_coefficient_of_friction_isotr1417922001_martins_et_al(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionISOTR1417922001MartinsEtAl' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionISOTR1417922001MartinsEtAl

    @property
    def tooth_loss_factor(self) -> 'float':
        '''float: 'ToothLossFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothLossFactor

    @property
    def mesh_coefficient_of_friction_isotc60(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionISOTC60' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionISOTC60

    @property
    def mesh_coefficient_of_friction_drozdov_and_gavrikov(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionDrozdovAndGavrikov' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionDrozdovAndGavrikov

    @property
    def mesh_coefficient_of_friction_o_donoghue_and_cameron(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionODonoghueAndCameron' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionODonoghueAndCameron

    @property
    def mesh_coefficient_of_friction_benedict_and_kelley(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionBenedictAndKelley

    @property
    def mesh_coefficient_of_friction_misharin(self) -> 'float':
        '''float: 'MeshCoefficientOfFrictionMisharin' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshCoefficientOfFrictionMisharin

    @property
    def load_intensity(self) -> 'float':
        '''float: 'LoadIntensity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadIntensity

    @property
    def load_sharing_factor_source(self) -> '_302.PlanetaryRatingLoadSharingOption':
        '''PlanetaryRatingLoadSharingOption: 'LoadSharingFactorSource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.LoadSharingFactorSource)
        return constructor.new(_302.PlanetaryRatingLoadSharingOption)(value) if value else None

    @property
    def load_sharing_factor(self) -> 'float':
        '''float: 'LoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadSharingFactor

    @property
    def cylindrical_mesh_single_flank_rating(self) -> '_426.CylindricalMeshSingleFlankRating':
        '''CylindricalMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _426.CylindricalMeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to CylindricalMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(self) -> '_446.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating':
        '''MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _446.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_plastic_gear_vdi2736_abstract_mesh_single_flank_rating(self) -> '_448.PlasticGearVDI2736AbstractMeshSingleFlankRating':
        '''PlasticGearVDI2736AbstractMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _448.PlasticGearVDI2736AbstractMeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to PlasticGearVDI2736AbstractMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_plastic_plastic_vdi2736_mesh_single_flank_rating(self) -> '_450.PlasticPlasticVDI2736MeshSingleFlankRating':
        '''PlasticPlasticVDI2736MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _450.PlasticPlasticVDI2736MeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to PlasticPlasticVDI2736MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso63361996_mesh_single_flank_rating(self) -> '_467.ISO63361996MeshSingleFlankRating':
        '''ISO63361996MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _467.ISO63361996MeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO63361996MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso63362006_mesh_single_flank_rating(self) -> '_469.ISO63362006MeshSingleFlankRating':
        '''ISO63362006MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _469.ISO63362006MeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso63362019_mesh_single_flank_rating(self) -> '_471.ISO63362019MeshSingleFlankRating':
        '''ISO63362019MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _471.ISO63362019MeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO63362019MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso6336_abstract_mesh_single_flank_rating(self) -> '_473.ISO6336AbstractMeshSingleFlankRating':
        '''ISO6336AbstractMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _473.ISO6336AbstractMeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO6336AbstractMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso6336_abstract_metal_mesh_single_flank_rating(self) -> '_475.ISO6336AbstractMetalMeshSingleFlankRating':
        '''ISO6336AbstractMetalMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _475.ISO6336AbstractMetalMeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO6336AbstractMetalMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_din3990_mesh_single_flank_rating(self) -> '_482.DIN3990MeshSingleFlankRating':
        '''DIN3990MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _482.DIN3990MeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to DIN3990MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_agma2101_mesh_single_flank_rating(self) -> '_484.AGMA2101MeshSingleFlankRating':
        '''AGMA2101MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _484.AGMA2101MeshSingleFlankRating.TYPE not in self.wrapped.CylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to AGMA2101MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.CylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalMeshSingleFlankRating.__class__)(self.wrapped.CylindricalMeshSingleFlankRating) if self.wrapped.CylindricalMeshSingleFlankRating else None

    @property
    def mesh_load_case(self) -> '_820.CylindricalMeshLoadCase':
        '''CylindricalMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalMeshLoadCase)(self.wrapped.MeshLoadCase) if self.wrapped.MeshLoadCase else None

    @property
    def gear_set_rating(self) -> '_423.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'GearSetRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_423.CylindricalGearSetRating)(self.wrapped.GearSetRating) if self.wrapped.GearSetRating else None

    @property
    def vdi_cylindrical_gear_single_flank_rating(self) -> '_445.VDI2737InternalGearSingleFlankRating':
        '''VDI2737InternalGearSingleFlankRating: 'VDICylindricalGearSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_445.VDI2737InternalGearSingleFlankRating)(self.wrapped.VDICylindricalGearSingleFlankRating) if self.wrapped.VDICylindricalGearSingleFlankRating else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating(self) -> '_475.ISO6336AbstractMetalMeshSingleFlankRating':
        '''ISO6336AbstractMetalMeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _475.ISO6336AbstractMetalMeshSingleFlankRating.TYPE not in self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO6336AbstractMetalMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__)(self.wrapped.ISODINCylindricalMeshSingleFlankRating) if self.wrapped.ISODINCylindricalMeshSingleFlankRating else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_iso63361996_mesh_single_flank_rating(self) -> '_467.ISO63361996MeshSingleFlankRating':
        '''ISO63361996MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _467.ISO63361996MeshSingleFlankRating.TYPE not in self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO63361996MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__)(self.wrapped.ISODINCylindricalMeshSingleFlankRating) if self.wrapped.ISODINCylindricalMeshSingleFlankRating else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_iso63362006_mesh_single_flank_rating(self) -> '_469.ISO63362006MeshSingleFlankRating':
        '''ISO63362006MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _469.ISO63362006MeshSingleFlankRating.TYPE not in self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__)(self.wrapped.ISODINCylindricalMeshSingleFlankRating) if self.wrapped.ISODINCylindricalMeshSingleFlankRating else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_iso63362019_mesh_single_flank_rating(self) -> '_471.ISO63362019MeshSingleFlankRating':
        '''ISO63362019MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _471.ISO63362019MeshSingleFlankRating.TYPE not in self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO63362019MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__)(self.wrapped.ISODINCylindricalMeshSingleFlankRating) if self.wrapped.ISODINCylindricalMeshSingleFlankRating else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_din3990_mesh_single_flank_rating(self) -> '_482.DIN3990MeshSingleFlankRating':
        '''DIN3990MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _482.DIN3990MeshSingleFlankRating.TYPE not in self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to DIN3990MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ISODINCylindricalMeshSingleFlankRating.__class__)(self.wrapped.ISODINCylindricalMeshSingleFlankRating) if self.wrapped.ISODINCylindricalMeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating(self) -> '_426.CylindricalMeshSingleFlankRating':
        '''CylindricalMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _426.CylindricalMeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to CylindricalMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(self) -> '_446.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating':
        '''MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _446.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_plastic_gear_vdi2736_abstract_mesh_single_flank_rating(self) -> '_448.PlasticGearVDI2736AbstractMeshSingleFlankRating':
        '''PlasticGearVDI2736AbstractMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _448.PlasticGearVDI2736AbstractMeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to PlasticGearVDI2736AbstractMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_plastic_plastic_vdi2736_mesh_single_flank_rating(self) -> '_450.PlasticPlasticVDI2736MeshSingleFlankRating':
        '''PlasticPlasticVDI2736MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _450.PlasticPlasticVDI2736MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to PlasticPlasticVDI2736MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_iso63361996_mesh_single_flank_rating(self) -> '_467.ISO63361996MeshSingleFlankRating':
        '''ISO63361996MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _467.ISO63361996MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63361996MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_iso63362006_mesh_single_flank_rating(self) -> '_469.ISO63362006MeshSingleFlankRating':
        '''ISO63362006MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _469.ISO63362006MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_iso63362019_mesh_single_flank_rating(self) -> '_471.ISO63362019MeshSingleFlankRating':
        '''ISO63362019MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _471.ISO63362019MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63362019MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_iso6336_abstract_mesh_single_flank_rating(self) -> '_473.ISO6336AbstractMeshSingleFlankRating':
        '''ISO6336AbstractMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _473.ISO6336AbstractMeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO6336AbstractMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_iso6336_abstract_metal_mesh_single_flank_rating(self) -> '_475.ISO6336AbstractMetalMeshSingleFlankRating':
        '''ISO6336AbstractMetalMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _475.ISO6336AbstractMetalMeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO6336AbstractMetalMeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_din3990_mesh_single_flank_rating(self) -> '_482.DIN3990MeshSingleFlankRating':
        '''DIN3990MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _482.DIN3990MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to DIN3990MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def mesh_single_flank_rating_of_type_agma2101_mesh_single_flank_rating(self) -> '_484.AGMA2101MeshSingleFlankRating':
        '''AGMA2101MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _484.AGMA2101MeshSingleFlankRating.TYPE not in self.wrapped.MeshSingleFlankRating.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to AGMA2101MeshSingleFlankRating. Expected: {}.'.format(self.wrapped.MeshSingleFlankRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MeshSingleFlankRating.__class__)(self.wrapped.MeshSingleFlankRating) if self.wrapped.MeshSingleFlankRating else None

    @property
    def agma_cylindrical_mesh_single_flank_rating(self) -> '_484.AGMA2101MeshSingleFlankRating':
        '''AGMA2101MeshSingleFlankRating: 'AGMACylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_484.AGMA2101MeshSingleFlankRating)(self.wrapped.AGMACylindricalMeshSingleFlankRating) if self.wrapped.AGMACylindricalMeshSingleFlankRating else None

    @property
    def cylindrical_gear_mesh(self) -> '_949.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'CylindricalGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_949.CylindricalGearMeshDesign)(self.wrapped.CylindricalGearMesh) if self.wrapped.CylindricalGearMesh else None

    @property
    def cylindrical_gear_ratings(self) -> 'List[_418.CylindricalGearRating]':
        '''List[CylindricalGearRating]: 'CylindricalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearRatings, constructor.new(_418.CylindricalGearRating))
        return value
