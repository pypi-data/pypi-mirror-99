﻿'''_6656.py

AssemblyAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model import _2112, _2151
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6454, _6586
from mastapy.system_model.analyses_and_results.system_deflections import _2365, _2466
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _6658, _6660, _6663, _6669,
    _6670, _6671, _6676, _6681,
    _6690, _6693, _6694, _6699,
    _6705, _6706, _6707, _6715,
    _6722, _6725, _6726, _6727,
    _6729, _6731, _6736, _6737,
    _6738, _6747, _6740, _6743,
    _6746, _6752, _6753, _6758,
    _6761, _6764, _6768, _6772,
    _6776, _6779, _6646
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'AssemblyAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyAdvancedTimeSteppingAnalysisForModulation',)


class AssemblyAdvancedTimeSteppingAnalysisForModulation(_6646.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation):
    '''AssemblyAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2112.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6454.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6454.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2365.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2365.AssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def bearings(self) -> 'List[_6658.BearingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BearingAdvancedTimeSteppingAnalysisForModulation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6658.BearingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def belt_drives(self) -> 'List[_6660.BeltDriveAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BeltDriveAdvancedTimeSteppingAnalysisForModulation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6660.BeltDriveAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6663.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6663.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolts(self) -> 'List[_6669.BoltAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltAdvancedTimeSteppingAnalysisForModulation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6669.BoltAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolted_joints(self) -> 'List[_6670.BoltedJointAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltedJointAdvancedTimeSteppingAnalysisForModulation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6670.BoltedJointAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def clutches(self) -> 'List[_6671.ClutchAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ClutchAdvancedTimeSteppingAnalysisForModulation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6671.ClutchAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_couplings(self) -> 'List[_6676.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptCouplingAdvancedTimeSteppingAnalysisForModulation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6676.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6681.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6681.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cv_ts(self) -> 'List[_6690.CVTAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CVTAdvancedTimeSteppingAnalysisForModulation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6690.CVTAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6693.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6693.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6694.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalDiscAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6694.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6699.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6699.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6705.FaceGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearSetAdvancedTimeSteppingAnalysisForModulation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6705.FaceGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def fe_parts(self) -> 'List[_6706.FEPartAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FEPartAdvancedTimeSteppingAnalysisForModulation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6706.FEPartAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6707.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6707.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6715.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6715.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6722.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6722.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6725.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6725.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def mass_discs(self) -> 'List[_6726.MassDiscAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MassDiscAdvancedTimeSteppingAnalysisForModulation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6726.MassDiscAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def measurement_components(self) -> 'List[_6727.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6727.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def oil_seals(self) -> 'List[_6729.OilSealAdvancedTimeSteppingAnalysisForModulation]':
        '''List[OilSealAdvancedTimeSteppingAnalysisForModulation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6729.OilSealAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6731.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6731.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def planet_carriers(self) -> 'List[_6736.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PlanetCarrierAdvancedTimeSteppingAnalysisForModulation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6736.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def point_loads(self) -> 'List[_6737.PointLoadAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PointLoadAdvancedTimeSteppingAnalysisForModulation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6737.PointLoadAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def power_loads(self) -> 'List[_6738.PowerLoadAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PowerLoadAdvancedTimeSteppingAnalysisForModulation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6738.PowerLoadAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6747.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6747.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def ring_pins(self) -> 'List[_6740.RingPinsAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RingPinsAdvancedTimeSteppingAnalysisForModulation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6740.RingPinsAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6743.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6743.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shafts(self) -> 'List[_6746.ShaftAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftAdvancedTimeSteppingAnalysisForModulation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6746.ShaftAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6752.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6752.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spring_dampers(self) -> 'List[_6753.SpringDamperAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpringDamperAdvancedTimeSteppingAnalysisForModulation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6753.SpringDamperAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6758.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6758.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6761.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6761.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def synchronisers(self) -> 'List[_6764.SynchroniserAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SynchroniserAdvancedTimeSteppingAnalysisForModulation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6764.SynchroniserAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def torque_converters(self) -> 'List[_6768.TorqueConverterAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterAdvancedTimeSteppingAnalysisForModulation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6768.TorqueConverterAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6772.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation]':
        '''List[UnbalancedMassAdvancedTimeSteppingAnalysisForModulation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6772.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6776.WormGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[WormGearSetAdvancedTimeSteppingAnalysisForModulation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6776.WormGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6779.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6779.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
