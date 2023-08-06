﻿'''_3803.py

AssemblyCompoundPowerFlow
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2083, _2122
from mastapy._internal.cast_exception import CastException
from mastapy.gears.analysis import _1134
from mastapy.system_model.analyses_and_results.power_flows import _3670
from mastapy.system_model.analyses_and_results.power_flows.compound import (
    _3804, _3806, _3809, _3815,
    _3816, _3817, _3822, _3827,
    _3837, _3839, _3841, _3845,
    _3851, _3852, _3853, _3860,
    _3867, _3870, _3871, _3872,
    _3874, _3876, _3881, _3882,
    _3883, _3892, _3885, _3887,
    _3891, _3897, _3898, _3903,
    _3906, _3909, _3913, _3917,
    _3921, _3924, _3796
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundPowerFlow',)


class AssemblyCompoundPowerFlow(_3796.AbstractAssemblyCompoundPowerFlow):
    '''AssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def input_power_load_ratio_warning(self) -> 'str':
        '''str: 'InputPowerLoadRatioWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InputPowerLoadRatioWarning

    @property
    def output_power_load_ratio_warning(self) -> 'str':
        '''str: 'OutputPowerLoadRatioWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OutputPowerLoadRatioWarning

    @property
    def component_design(self) -> '_2083.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2083.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def rating_for_all_gear_sets(self) -> '_1134.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1134.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3670.AssemblyPowerFlow]':
        '''List[AssemblyPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3670.AssemblyPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3670.AssemblyPowerFlow]':
        '''List[AssemblyPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3670.AssemblyPowerFlow))
        return value

    @property
    def bearings(self) -> 'List[_3804.BearingCompoundPowerFlow]':
        '''List[BearingCompoundPowerFlow]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3804.BearingCompoundPowerFlow))
        return value

    @property
    def belt_drives(self) -> 'List[_3806.BeltDriveCompoundPowerFlow]':
        '''List[BeltDriveCompoundPowerFlow]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3806.BeltDriveCompoundPowerFlow))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3809.BevelDifferentialGearSetCompoundPowerFlow]':
        '''List[BevelDifferentialGearSetCompoundPowerFlow]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3809.BevelDifferentialGearSetCompoundPowerFlow))
        return value

    @property
    def bolts(self) -> 'List[_3815.BoltCompoundPowerFlow]':
        '''List[BoltCompoundPowerFlow]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3815.BoltCompoundPowerFlow))
        return value

    @property
    def bolted_joints(self) -> 'List[_3816.BoltedJointCompoundPowerFlow]':
        '''List[BoltedJointCompoundPowerFlow]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3816.BoltedJointCompoundPowerFlow))
        return value

    @property
    def clutches(self) -> 'List[_3817.ClutchCompoundPowerFlow]':
        '''List[ClutchCompoundPowerFlow]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3817.ClutchCompoundPowerFlow))
        return value

    @property
    def concept_couplings(self) -> 'List[_3822.ConceptCouplingCompoundPowerFlow]':
        '''List[ConceptCouplingCompoundPowerFlow]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3822.ConceptCouplingCompoundPowerFlow))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3827.ConceptGearSetCompoundPowerFlow]':
        '''List[ConceptGearSetCompoundPowerFlow]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3827.ConceptGearSetCompoundPowerFlow))
        return value

    @property
    def cv_ts(self) -> 'List[_3837.CVTCompoundPowerFlow]':
        '''List[CVTCompoundPowerFlow]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3837.CVTCompoundPowerFlow))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3839.CycloidalAssemblyCompoundPowerFlow]':
        '''List[CycloidalAssemblyCompoundPowerFlow]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3839.CycloidalAssemblyCompoundPowerFlow))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3841.CycloidalDiscCompoundPowerFlow]':
        '''List[CycloidalDiscCompoundPowerFlow]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3841.CycloidalDiscCompoundPowerFlow))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3845.CylindricalGearSetCompoundPowerFlow]':
        '''List[CylindricalGearSetCompoundPowerFlow]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3845.CylindricalGearSetCompoundPowerFlow))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3851.FaceGearSetCompoundPowerFlow]':
        '''List[FaceGearSetCompoundPowerFlow]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3851.FaceGearSetCompoundPowerFlow))
        return value

    @property
    def fe_parts(self) -> 'List[_3852.FEPartCompoundPowerFlow]':
        '''List[FEPartCompoundPowerFlow]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3852.FEPartCompoundPowerFlow))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3853.FlexiblePinAssemblyCompoundPowerFlow]':
        '''List[FlexiblePinAssemblyCompoundPowerFlow]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3853.FlexiblePinAssemblyCompoundPowerFlow))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3860.HypoidGearSetCompoundPowerFlow]':
        '''List[HypoidGearSetCompoundPowerFlow]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3860.HypoidGearSetCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3867.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3867.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3870.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3870.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow))
        return value

    @property
    def mass_discs(self) -> 'List[_3871.MassDiscCompoundPowerFlow]':
        '''List[MassDiscCompoundPowerFlow]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3871.MassDiscCompoundPowerFlow))
        return value

    @property
    def measurement_components(self) -> 'List[_3872.MeasurementComponentCompoundPowerFlow]':
        '''List[MeasurementComponentCompoundPowerFlow]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3872.MeasurementComponentCompoundPowerFlow))
        return value

    @property
    def oil_seals(self) -> 'List[_3874.OilSealCompoundPowerFlow]':
        '''List[OilSealCompoundPowerFlow]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3874.OilSealCompoundPowerFlow))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3876.PartToPartShearCouplingCompoundPowerFlow]':
        '''List[PartToPartShearCouplingCompoundPowerFlow]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3876.PartToPartShearCouplingCompoundPowerFlow))
        return value

    @property
    def planet_carriers(self) -> 'List[_3881.PlanetCarrierCompoundPowerFlow]':
        '''List[PlanetCarrierCompoundPowerFlow]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3881.PlanetCarrierCompoundPowerFlow))
        return value

    @property
    def point_loads(self) -> 'List[_3882.PointLoadCompoundPowerFlow]':
        '''List[PointLoadCompoundPowerFlow]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3882.PointLoadCompoundPowerFlow))
        return value

    @property
    def power_loads(self) -> 'List[_3883.PowerLoadCompoundPowerFlow]':
        '''List[PowerLoadCompoundPowerFlow]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3883.PowerLoadCompoundPowerFlow))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3892.ShaftHubConnectionCompoundPowerFlow]':
        '''List[ShaftHubConnectionCompoundPowerFlow]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3892.ShaftHubConnectionCompoundPowerFlow))
        return value

    @property
    def ring_pins(self) -> 'List[_3885.RingPinsCompoundPowerFlow]':
        '''List[RingPinsCompoundPowerFlow]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3885.RingPinsCompoundPowerFlow))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3887.RollingRingAssemblyCompoundPowerFlow]':
        '''List[RollingRingAssemblyCompoundPowerFlow]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3887.RollingRingAssemblyCompoundPowerFlow))
        return value

    @property
    def shafts(self) -> 'List[_3891.ShaftCompoundPowerFlow]':
        '''List[ShaftCompoundPowerFlow]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3891.ShaftCompoundPowerFlow))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3897.SpiralBevelGearSetCompoundPowerFlow]':
        '''List[SpiralBevelGearSetCompoundPowerFlow]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3897.SpiralBevelGearSetCompoundPowerFlow))
        return value

    @property
    def spring_dampers(self) -> 'List[_3898.SpringDamperCompoundPowerFlow]':
        '''List[SpringDamperCompoundPowerFlow]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3898.SpringDamperCompoundPowerFlow))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3903.StraightBevelDiffGearSetCompoundPowerFlow]':
        '''List[StraightBevelDiffGearSetCompoundPowerFlow]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3903.StraightBevelDiffGearSetCompoundPowerFlow))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3906.StraightBevelGearSetCompoundPowerFlow]':
        '''List[StraightBevelGearSetCompoundPowerFlow]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3906.StraightBevelGearSetCompoundPowerFlow))
        return value

    @property
    def synchronisers(self) -> 'List[_3909.SynchroniserCompoundPowerFlow]':
        '''List[SynchroniserCompoundPowerFlow]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3909.SynchroniserCompoundPowerFlow))
        return value

    @property
    def torque_converters(self) -> 'List[_3913.TorqueConverterCompoundPowerFlow]':
        '''List[TorqueConverterCompoundPowerFlow]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3913.TorqueConverterCompoundPowerFlow))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3917.UnbalancedMassCompoundPowerFlow]':
        '''List[UnbalancedMassCompoundPowerFlow]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3917.UnbalancedMassCompoundPowerFlow))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3921.WormGearSetCompoundPowerFlow]':
        '''List[WormGearSetCompoundPowerFlow]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3921.WormGearSetCompoundPowerFlow))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3924.ZerolBevelGearSetCompoundPowerFlow]':
        '''List[ZerolBevelGearSetCompoundPowerFlow]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3924.ZerolBevelGearSetCompoundPowerFlow))
        return value
