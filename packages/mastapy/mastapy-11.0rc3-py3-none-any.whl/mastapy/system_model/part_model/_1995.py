﻿'''_1995.py

Assembly
'''


from typing import List, TypeVar, Optional

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2023, _2004, _2000, _2003,
    _2016, _2030, _2029, _2024,
    _2026, _1996, _1997, _2002,
    _2007, _2008, _2011, _2012,
    _2013, _2020, _2021, _2022,
    _2027, _2032, _2034, _2035,
    _2036
)
from mastapy.system_model.part_model.gears import (
    _2104, _2091, _2100, _2082,
    _2080, _2108, _2093, _2069,
    _2070, _2071, _2072, _2073,
    _2074, _2075, _2076, _2077,
    _2078, _2079, _2081, _2083,
    _2084, _2085, _2086, _2088,
    _2090, _2092, _2094, _2095,
    _2096, _2097, _2098, _2099,
    _2101, _2102, _2103, _2105,
    _2106, _2107, _2109, _2110
)
from mastapy.system_model.part_model.couplings import (
    _2149, _2128, _2130, _2131,
    _2133, _2134, _2135, _2136,
    _2137, _2138, _2139, _2140,
    _2141, _2147, _2148, _2150,
    _2151, _2152, _2154, _2155,
    _2156, _2157, _2158, _2160
)
from mastapy.system_model.part_model.shaft_model import _2039
from mastapy.system_model.part_model.creation_options import (
    _2124, _2126, _2127, _2125
)
from mastapy.gears.gear_designs.creation_options import _883, _886
from mastapy.gears import _135
from mastapy.gears.gear_designs.bevel import _916
from mastapy.nodal_analysis import _1390
from mastapy.bearings import _1509, _1534
from mastapy._internal.python_net import python_net_import

_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')


__docformat__ = 'restructuredtext en'
__all__ = ('Assembly',)


class Assembly(_1996.AbstractAssembly):
    '''Assembly

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Assembly.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def face_width_of_widest_cylindrical_gear(self) -> 'float':
        '''float: 'FaceWidthOfWidestCylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceWidthOfWidestCylindricalGear

    @property
    def mass_of_gears(self) -> 'float':
        '''float: 'MassOfGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfGears

    @property
    def mass_of_bearings(self) -> 'float':
        '''float: 'MassOfBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfBearings

    @property
    def mass_of_shafts(self) -> 'float':
        '''float: 'MassOfShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfShafts

    @property
    def mass_of_imported_fe_shafts(self) -> 'float':
        '''float: 'MassOfImportedFEShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfImportedFEShafts

    @property
    def mass_of_imported_fe_housings(self) -> 'float':
        '''float: 'MassOfImportedFEHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfImportedFEHousings

    @property
    def mass_of_other_parts(self) -> 'float':
        '''float: 'MassOfOtherParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfOtherParts

    @property
    def smallest_number_of_teeth(self) -> 'int':
        '''int: 'SmallestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestNumberOfTeeth

    @property
    def largest_number_of_teeth(self) -> 'int':
        '''int: 'LargestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LargestNumberOfTeeth

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseAndAxialContactRatioRatingForNVH

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatioRatingForNVH

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialContactRatioRatingForNVH

    @property
    def minimum_tip_thickness(self) -> 'float':
        '''float: 'MinimumTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTipThickness

    @property
    def oil_level_specification(self) -> '_2023.OilLevelSpecification':
        '''OilLevelSpecification: 'OilLevelSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2023.OilLevelSpecification)(self.wrapped.OilLevelSpecification) if self.wrapped.OilLevelSpecification else None

    @property
    def components_with_unknown_scalar_mass(self) -> 'List[_2004.Component]':
        '''List[Component]: 'ComponentsWithUnknownScalarMass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentsWithUnknownScalarMass, constructor.new(_2004.Component))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2104.StraightBevelGearSet]':
        '''List[StraightBevelGearSet]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2104.StraightBevelGearSet))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2091.HypoidGearSet]':
        '''List[HypoidGearSet]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2091.HypoidGearSet))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2100.SpiralBevelGearSet]':
        '''List[SpiralBevelGearSet]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2100.SpiralBevelGearSet))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2149.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2149.ShaftHubConnection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2082.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2082.CylindricalGearSet))
        return value

    @property
    def conical_gear_sets(self) -> 'List[_2080.ConicalGearSet]':
        '''List[ConicalGearSet]: 'ConicalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGearSets, constructor.new(_2080.ConicalGearSet))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2108.WormGearSet]':
        '''List[WormGearSet]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2108.WormGearSet))
        return value

    @property
    def klingelnberg_cyclo_palloid_gear_sets(self) -> 'List[_2093.KlingelnbergCycloPalloidConicalGearSet]':
        '''List[KlingelnbergCycloPalloidConicalGearSet]: 'KlingelnbergCycloPalloidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidGearSets, constructor.new(_2093.KlingelnbergCycloPalloidConicalGearSet))
        return value

    @property
    def shafts(self) -> 'List[_2039.Shaft]':
        '''List[Shaft]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2039.Shaft))
        return value

    @property
    def bearings(self) -> 'List[_2000.Bearing]':
        '''List[Bearing]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2000.Bearing))
        return value

    @property
    def bolted_joints(self) -> 'List[_2003.BoltedJoint]':
        '''List[BoltedJoint]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2003.BoltedJoint))
        return value

    @property
    def imported_fes(self) -> 'List[_2016.ImportedFEComponent]':
        '''List[ImportedFEComponent]: 'ImportedFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEs, constructor.new(_2016.ImportedFEComponent))
        return value

    @property
    def component_details(self) -> 'List[_2004.Component]':
        '''List[Component]: 'ComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDetails, constructor.new(_2004.Component))
        return value

    @property
    def power_loads(self) -> 'List[_2030.PowerLoad]':
        '''List[PowerLoad]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2030.PowerLoad))
        return value

    @property
    def point_loads(self) -> 'List[_2029.PointLoad]':
        '''List[PointLoad]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2029.PointLoad))
        return value

    @property
    def oil_seals(self) -> 'List[_2024.OilSeal]':
        '''List[OilSeal]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2024.OilSeal))
        return value

    def get_part_named(self, name: 'str') -> '_2026.Part':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Part
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2026.Part.TYPE](name if name else None)
        return constructor.new(_2026.Part)(method_result) if method_result else None

    def get_part_named_of_type_assembly(self, name: 'str') -> 'Assembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[Assembly.TYPE](name if name else None)
        return constructor.new(Assembly)(method_result) if method_result else None

    def get_part_named_of_type_abstract_assembly(self, name: 'str') -> '_1996.AbstractAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1996.AbstractAssembly.TYPE](name if name else None)
        return constructor.new(_1996.AbstractAssembly)(method_result) if method_result else None

    def get_part_named_of_type_abstract_shaft_or_housing(self, name: 'str') -> '_1997.AbstractShaftOrHousing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractShaftOrHousing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1997.AbstractShaftOrHousing.TYPE](name if name else None)
        return constructor.new(_1997.AbstractShaftOrHousing)(method_result) if method_result else None

    def get_part_named_of_type_bearing(self, name: 'str') -> '_2000.Bearing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2000.Bearing.TYPE](name if name else None)
        return constructor.new(_2000.Bearing)(method_result) if method_result else None

    def get_part_named_of_type_bolt(self, name: 'str') -> '_2002.Bolt':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bolt
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2002.Bolt.TYPE](name if name else None)
        return constructor.new(_2002.Bolt)(method_result) if method_result else None

    def get_part_named_of_type_bolted_joint(self, name: 'str') -> '_2003.BoltedJoint':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2003.BoltedJoint.TYPE](name if name else None)
        return constructor.new(_2003.BoltedJoint)(method_result) if method_result else None

    def get_part_named_of_type_component(self, name: 'str') -> '_2004.Component':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2004.Component.TYPE](name if name else None)
        return constructor.new(_2004.Component)(method_result) if method_result else None

    def get_part_named_of_type_connector(self, name: 'str') -> '_2007.Connector':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Connector
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2007.Connector.TYPE](name if name else None)
        return constructor.new(_2007.Connector)(method_result) if method_result else None

    def get_part_named_of_type_datum(self, name: 'str') -> '_2008.Datum':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2008.Datum.TYPE](name if name else None)
        return constructor.new(_2008.Datum)(method_result) if method_result else None

    def get_part_named_of_type_external_cad_model(self, name: 'str') -> '_2011.ExternalCADModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.ExternalCADModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2011.ExternalCADModel.TYPE](name if name else None)
        return constructor.new(_2011.ExternalCADModel)(method_result) if method_result else None

    def get_part_named_of_type_flexible_pin_assembly(self, name: 'str') -> '_2012.FlexiblePinAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.FlexiblePinAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2012.FlexiblePinAssembly.TYPE](name if name else None)
        return constructor.new(_2012.FlexiblePinAssembly)(method_result) if method_result else None

    def get_part_named_of_type_guide_dxf_model(self, name: 'str') -> '_2013.GuideDxfModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.GuideDxfModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2013.GuideDxfModel.TYPE](name if name else None)
        return constructor.new(_2013.GuideDxfModel)(method_result) if method_result else None

    def get_part_named_of_type_imported_fe_component(self, name: 'str') -> '_2016.ImportedFEComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2016.ImportedFEComponent.TYPE](name if name else None)
        return constructor.new(_2016.ImportedFEComponent)(method_result) if method_result else None

    def get_part_named_of_type_mass_disc(self, name: 'str') -> '_2020.MassDisc':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2020.MassDisc.TYPE](name if name else None)
        return constructor.new(_2020.MassDisc)(method_result) if method_result else None

    def get_part_named_of_type_measurement_component(self, name: 'str') -> '_2021.MeasurementComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2021.MeasurementComponent.TYPE](name if name else None)
        return constructor.new(_2021.MeasurementComponent)(method_result) if method_result else None

    def get_part_named_of_type_mountable_component(self, name: 'str') -> '_2022.MountableComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MountableComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2022.MountableComponent.TYPE](name if name else None)
        return constructor.new(_2022.MountableComponent)(method_result) if method_result else None

    def get_part_named_of_type_oil_seal(self, name: 'str') -> '_2024.OilSeal':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2024.OilSeal.TYPE](name if name else None)
        return constructor.new(_2024.OilSeal)(method_result) if method_result else None

    def get_part_named_of_type_planet_carrier(self, name: 'str') -> '_2027.PlanetCarrier':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2027.PlanetCarrier.TYPE](name if name else None)
        return constructor.new(_2027.PlanetCarrier)(method_result) if method_result else None

    def get_part_named_of_type_point_load(self, name: 'str') -> '_2029.PointLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2029.PointLoad.TYPE](name if name else None)
        return constructor.new(_2029.PointLoad)(method_result) if method_result else None

    def get_part_named_of_type_power_load(self, name: 'str') -> '_2030.PowerLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2030.PowerLoad.TYPE](name if name else None)
        return constructor.new(_2030.PowerLoad)(method_result) if method_result else None

    def get_part_named_of_type_root_assembly(self, name: 'str') -> '_2032.RootAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.RootAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2032.RootAssembly.TYPE](name if name else None)
        return constructor.new(_2032.RootAssembly)(method_result) if method_result else None

    def get_part_named_of_type_specialised_assembly(self, name: 'str') -> '_2034.SpecialisedAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.SpecialisedAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2034.SpecialisedAssembly.TYPE](name if name else None)
        return constructor.new(_2034.SpecialisedAssembly)(method_result) if method_result else None

    def get_part_named_of_type_unbalanced_mass(self, name: 'str') -> '_2035.UnbalancedMass':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2035.UnbalancedMass.TYPE](name if name else None)
        return constructor.new(_2035.UnbalancedMass)(method_result) if method_result else None

    def get_part_named_of_type_virtual_component(self, name: 'str') -> '_2036.VirtualComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.VirtualComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2036.VirtualComponent.TYPE](name if name else None)
        return constructor.new(_2036.VirtualComponent)(method_result) if method_result else None

    def get_part_named_of_type_shaft(self, name: 'str') -> '_2039.Shaft':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2039.Shaft.TYPE](name if name else None)
        return constructor.new(_2039.Shaft)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear(self, name: 'str') -> '_2069.AGMAGleasonConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2069.AGMAGleasonConicalGear.TYPE](name if name else None)
        return constructor.new(_2069.AGMAGleasonConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear_set(self, name: 'str') -> '_2070.AGMAGleasonConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2070.AGMAGleasonConicalGearSet.TYPE](name if name else None)
        return constructor.new(_2070.AGMAGleasonConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear(self, name: 'str') -> '_2071.BevelDifferentialGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2071.BevelDifferentialGear.TYPE](name if name else None)
        return constructor.new(_2071.BevelDifferentialGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear_set(self, name: 'str') -> '_2072.BevelDifferentialGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2072.BevelDifferentialGearSet.TYPE](name if name else None)
        return constructor.new(_2072.BevelDifferentialGearSet)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_planet_gear(self, name: 'str') -> '_2073.BevelDifferentialPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2073.BevelDifferentialPlanetGear.TYPE](name if name else None)
        return constructor.new(_2073.BevelDifferentialPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_sun_gear(self, name: 'str') -> '_2074.BevelDifferentialSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2074.BevelDifferentialSunGear.TYPE](name if name else None)
        return constructor.new(_2074.BevelDifferentialSunGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear(self, name: 'str') -> '_2075.BevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2075.BevelGear.TYPE](name if name else None)
        return constructor.new(_2075.BevelGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear_set(self, name: 'str') -> '_2076.BevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2076.BevelGearSet.TYPE](name if name else None)
        return constructor.new(_2076.BevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear(self, name: 'str') -> '_2077.ConceptGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2077.ConceptGear.TYPE](name if name else None)
        return constructor.new(_2077.ConceptGear)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear_set(self, name: 'str') -> '_2078.ConceptGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2078.ConceptGearSet.TYPE](name if name else None)
        return constructor.new(_2078.ConceptGearSet)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear(self, name: 'str') -> '_2079.ConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2079.ConicalGear.TYPE](name if name else None)
        return constructor.new(_2079.ConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear_set(self, name: 'str') -> '_2080.ConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2080.ConicalGearSet.TYPE](name if name else None)
        return constructor.new(_2080.ConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear(self, name: 'str') -> '_2081.CylindricalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2081.CylindricalGear.TYPE](name if name else None)
        return constructor.new(_2081.CylindricalGear)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear_set(self, name: 'str') -> '_2082.CylindricalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2082.CylindricalGearSet.TYPE](name if name else None)
        return constructor.new(_2082.CylindricalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_planet_gear(self, name: 'str') -> '_2083.CylindricalPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2083.CylindricalPlanetGear.TYPE](name if name else None)
        return constructor.new(_2083.CylindricalPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_face_gear(self, name: 'str') -> '_2084.FaceGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2084.FaceGear.TYPE](name if name else None)
        return constructor.new(_2084.FaceGear)(method_result) if method_result else None

    def get_part_named_of_type_face_gear_set(self, name: 'str') -> '_2085.FaceGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2085.FaceGearSet.TYPE](name if name else None)
        return constructor.new(_2085.FaceGearSet)(method_result) if method_result else None

    def get_part_named_of_type_gear(self, name: 'str') -> '_2086.Gear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.Gear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2086.Gear.TYPE](name if name else None)
        return constructor.new(_2086.Gear)(method_result) if method_result else None

    def get_part_named_of_type_gear_set(self, name: 'str') -> '_2088.GearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.GearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2088.GearSet.TYPE](name if name else None)
        return constructor.new(_2088.GearSet)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear(self, name: 'str') -> '_2090.HypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2090.HypoidGear.TYPE](name if name else None)
        return constructor.new(_2090.HypoidGear)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear_set(self, name: 'str') -> '_2091.HypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2091.HypoidGearSet.TYPE](name if name else None)
        return constructor.new(_2091.HypoidGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear(self, name: 'str') -> '_2092.KlingelnbergCycloPalloidConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2092.KlingelnbergCycloPalloidConicalGear.TYPE](name if name else None)
        return constructor.new(_2092.KlingelnbergCycloPalloidConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, name: 'str') -> '_2093.KlingelnbergCycloPalloidConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2093.KlingelnbergCycloPalloidConicalGearSet.TYPE](name if name else None)
        return constructor.new(_2093.KlingelnbergCycloPalloidConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, name: 'str') -> '_2094.KlingelnbergCycloPalloidHypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2094.KlingelnbergCycloPalloidHypoidGear.TYPE](name if name else None)
        return constructor.new(_2094.KlingelnbergCycloPalloidHypoidGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: 'str') -> '_2095.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2095.KlingelnbergCycloPalloidHypoidGearSet.TYPE](name if name else None)
        return constructor.new(_2095.KlingelnbergCycloPalloidHypoidGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, name: 'str') -> '_2096.KlingelnbergCycloPalloidSpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2096.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](name if name else None)
        return constructor.new(_2096.KlingelnbergCycloPalloidSpiralBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: 'str') -> '_2097.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2097.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2097.KlingelnbergCycloPalloidSpiralBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_planetary_gear_set(self, name: 'str') -> '_2098.PlanetaryGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2098.PlanetaryGearSet.TYPE](name if name else None)
        return constructor.new(_2098.PlanetaryGearSet)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear(self, name: 'str') -> '_2099.SpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2099.SpiralBevelGear.TYPE](name if name else None)
        return constructor.new(_2099.SpiralBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear_set(self, name: 'str') -> '_2100.SpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2100.SpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2100.SpiralBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear(self, name: 'str') -> '_2101.StraightBevelDiffGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2101.StraightBevelDiffGear.TYPE](name if name else None)
        return constructor.new(_2101.StraightBevelDiffGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear_set(self, name: 'str') -> '_2102.StraightBevelDiffGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2102.StraightBevelDiffGearSet.TYPE](name if name else None)
        return constructor.new(_2102.StraightBevelDiffGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear(self, name: 'str') -> '_2103.StraightBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2103.StraightBevelGear.TYPE](name if name else None)
        return constructor.new(_2103.StraightBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear_set(self, name: 'str') -> '_2104.StraightBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2104.StraightBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2104.StraightBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_planet_gear(self, name: 'str') -> '_2105.StraightBevelPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2105.StraightBevelPlanetGear.TYPE](name if name else None)
        return constructor.new(_2105.StraightBevelPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_sun_gear(self, name: 'str') -> '_2106.StraightBevelSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2106.StraightBevelSunGear.TYPE](name if name else None)
        return constructor.new(_2106.StraightBevelSunGear)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear(self, name: 'str') -> '_2107.WormGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2107.WormGear.TYPE](name if name else None)
        return constructor.new(_2107.WormGear)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear_set(self, name: 'str') -> '_2108.WormGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2108.WormGearSet.TYPE](name if name else None)
        return constructor.new(_2108.WormGearSet)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear(self, name: 'str') -> '_2109.ZerolBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2109.ZerolBevelGear.TYPE](name if name else None)
        return constructor.new(_2109.ZerolBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear_set(self, name: 'str') -> '_2110.ZerolBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2110.ZerolBevelGearSet.TYPE](name if name else None)
        return constructor.new(_2110.ZerolBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_belt_drive(self, name: 'str') -> '_2128.BeltDrive':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2128.BeltDrive.TYPE](name if name else None)
        return constructor.new(_2128.BeltDrive)(method_result) if method_result else None

    def get_part_named_of_type_clutch(self, name: 'str') -> '_2130.Clutch':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2130.Clutch.TYPE](name if name else None)
        return constructor.new(_2130.Clutch)(method_result) if method_result else None

    def get_part_named_of_type_clutch_half(self, name: 'str') -> '_2131.ClutchHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ClutchHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2131.ClutchHalf.TYPE](name if name else None)
        return constructor.new(_2131.ClutchHalf)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling(self, name: 'str') -> '_2133.ConceptCoupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2133.ConceptCoupling.TYPE](name if name else None)
        return constructor.new(_2133.ConceptCoupling)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling_half(self, name: 'str') -> '_2134.ConceptCouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2134.ConceptCouplingHalf.TYPE](name if name else None)
        return constructor.new(_2134.ConceptCouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_coupling(self, name: 'str') -> '_2135.Coupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Coupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2135.Coupling.TYPE](name if name else None)
        return constructor.new(_2135.Coupling)(method_result) if method_result else None

    def get_part_named_of_type_coupling_half(self, name: 'str') -> '_2136.CouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2136.CouplingHalf.TYPE](name if name else None)
        return constructor.new(_2136.CouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_cvt(self, name: 'str') -> '_2137.CVT':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2137.CVT.TYPE](name if name else None)
        return constructor.new(_2137.CVT)(method_result) if method_result else None

    def get_part_named_of_type_cvt_pulley(self, name: 'str') -> '_2138.CVTPulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVTPulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2138.CVTPulley.TYPE](name if name else None)
        return constructor.new(_2138.CVTPulley)(method_result) if method_result else None

    def get_part_named_of_type_part_to_part_shear_coupling(self, name: 'str') -> '_2139.PartToPartShearCoupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.PartToPartShearCoupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2139.PartToPartShearCoupling.TYPE](name if name else None)
        return constructor.new(_2139.PartToPartShearCoupling)(method_result) if method_result else None

    def get_part_named_of_type_part_to_part_shear_coupling_half(self, name: 'str') -> '_2140.PartToPartShearCouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2140.PartToPartShearCouplingHalf.TYPE](name if name else None)
        return constructor.new(_2140.PartToPartShearCouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_pulley(self, name: 'str') -> '_2141.Pulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Pulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2141.Pulley.TYPE](name if name else None)
        return constructor.new(_2141.Pulley)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring(self, name: 'str') -> '_2147.RollingRing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2147.RollingRing.TYPE](name if name else None)
        return constructor.new(_2147.RollingRing)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring_assembly(self, name: 'str') -> '_2148.RollingRingAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRingAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2148.RollingRingAssembly.TYPE](name if name else None)
        return constructor.new(_2148.RollingRingAssembly)(method_result) if method_result else None

    def get_part_named_of_type_shaft_hub_connection(self, name: 'str') -> '_2149.ShaftHubConnection':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2149.ShaftHubConnection.TYPE](name if name else None)
        return constructor.new(_2149.ShaftHubConnection)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper(self, name: 'str') -> '_2150.SpringDamper':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2150.SpringDamper.TYPE](name if name else None)
        return constructor.new(_2150.SpringDamper)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper_half(self, name: 'str') -> '_2151.SpringDamperHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamperHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2151.SpringDamperHalf.TYPE](name if name else None)
        return constructor.new(_2151.SpringDamperHalf)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser(self, name: 'str') -> '_2152.Synchroniser':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2152.Synchroniser.TYPE](name if name else None)
        return constructor.new(_2152.Synchroniser)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_half(self, name: 'str') -> '_2154.SynchroniserHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2154.SynchroniserHalf.TYPE](name if name else None)
        return constructor.new(_2154.SynchroniserHalf)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_part(self, name: 'str') -> '_2155.SynchroniserPart':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserPart
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2155.SynchroniserPart.TYPE](name if name else None)
        return constructor.new(_2155.SynchroniserPart)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_sleeve(self, name: 'str') -> '_2156.SynchroniserSleeve':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserSleeve
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2156.SynchroniserSleeve.TYPE](name if name else None)
        return constructor.new(_2156.SynchroniserSleeve)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter(self, name: 'str') -> '_2157.TorqueConverter':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2157.TorqueConverter.TYPE](name if name else None)
        return constructor.new(_2157.TorqueConverter)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_pump(self, name: 'str') -> '_2158.TorqueConverterPump':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterPump
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2158.TorqueConverterPump.TYPE](name if name else None)
        return constructor.new(_2158.TorqueConverterPump)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_turbine(self, name: 'str') -> '_2160.TorqueConverterTurbine':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterTurbine
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2160.TorqueConverterTurbine.TYPE](name if name else None)
        return constructor.new(_2160.TorqueConverterTurbine)(method_result) if method_result else None

    def add_part(self, part_type: 'Assembly.PartType', name: 'str') -> '_2026.Part':
        ''' 'AddPart' is the original name of this method.

        Args:
            part_type (mastapy.system_model.part_model.Assembly.PartType)
            name (str)

        Returns:
            mastapy.system_model.part_model.Part
        '''

        part_type = conversion.mp_to_pn_enum(part_type)
        name = str(name)
        method_result = self.wrapped.AddPart(part_type, name if name else None)
        return constructor.new(_2026.Part)(method_result) if method_result else None

    def add_assembly(self, name: Optional['str'] = 'Assembly') -> 'Assembly':
        ''' 'AddAssembly' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.AddAssembly(name if name else None)
        return constructor.new(Assembly)(method_result) if method_result else None

    def add_oil_seal(self, name: Optional['str'] = 'Oil Seal') -> '_2024.OilSeal':
        ''' 'AddOilSeal' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.AddOilSeal(name if name else None)
        return constructor.new(_2024.OilSeal)(method_result) if method_result else None

    def add_power_load(self, name: Optional['str'] = 'Power Load') -> '_2030.PowerLoad':
        ''' 'AddPowerLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPowerLoad(name if name else None)
        return constructor.new(_2030.PowerLoad)(method_result) if method_result else None

    def add_point_load(self, name: Optional['str'] = 'Point Load') -> '_2029.PointLoad':
        ''' 'AddPointLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPointLoad(name if name else None)
        return constructor.new(_2029.PointLoad)(method_result) if method_result else None

    def add_datum(self, name: Optional['str'] = 'Datum') -> '_2008.Datum':
        ''' 'AddDatum' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.AddDatum(name if name else None)
        return constructor.new(_2008.Datum)(method_result) if method_result else None

    def add_imported_fe_component(self, name: Optional['str'] = 'Imported FE') -> '_2016.ImportedFEComponent':
        ''' 'AddImportedFEComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        name = str(name)
        method_result = self.wrapped.AddImportedFEComponent(name if name else None)
        return constructor.new(_2016.ImportedFEComponent)(method_result) if method_result else None

    def add_measurement_component(self, name: Optional['str'] = 'Measurement Component') -> '_2021.MeasurementComponent':
        ''' 'AddMeasurementComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.AddMeasurementComponent(name if name else None)
        return constructor.new(_2021.MeasurementComponent)(method_result) if method_result else None

    def add_mass_disc(self, name: Optional['str'] = 'Mass Disc') -> '_2020.MassDisc':
        ''' 'AddMassDisc' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.AddMassDisc(name if name else None)
        return constructor.new(_2020.MassDisc)(method_result) if method_result else None

    def add_unbalanced_mass(self, name: Optional['str'] = 'Unbalanced Mass') -> '_2035.UnbalancedMass':
        ''' 'AddUnbalancedMass' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.AddUnbalancedMass(name if name else None)
        return constructor.new(_2035.UnbalancedMass)(method_result) if method_result else None

    def add_straight_bevel_differential_gear_set(self, name: Optional['str'] = 'Straight Bevel Differential Gear Set') -> '_2102.StraightBevelDiffGearSet':
        ''' 'AddStraightBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelDifferentialGearSet(name if name else None)
        return constructor.new(_2102.StraightBevelDiffGearSet)(method_result) if method_result else None

    def add_spiral_bevel_differential_gear_set(self, name: Optional['str'] = 'Spiral Bevel Differential Gear Set') -> '_2072.BevelDifferentialGearSet':
        ''' 'AddSpiralBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelDifferentialGearSet(name if name else None)
        return constructor.new(_2072.BevelDifferentialGearSet)(method_result) if method_result else None

    def add_zerol_bevel_differential_gear_set(self, name: Optional['str'] = 'Zerol Bevel Differential Gear Set') -> '_2072.BevelDifferentialGearSet':
        ''' 'AddZerolBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelDifferentialGearSet(name if name else None)
        return constructor.new(_2072.BevelDifferentialGearSet)(method_result) if method_result else None

    def add_planetary_gear_set(self, name: Optional['str'] = 'Planetary Gear Set') -> '_2098.PlanetaryGearSet':
        ''' 'AddPlanetaryGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddPlanetaryGearSet(name if name else None)
        return constructor.new(_2098.PlanetaryGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set(self, name: Optional['str'] = 'Spiral Bevel Gear Set') -> '_2100.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelGearSet(name if name else None)
        return constructor.new(_2100.SpiralBevelGearSet)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Spiral Bevel Gear Set') -> '_2097.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'AddKlingelnbergCycloPalloidSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidSpiralBevelGearSet(name if name else None)
        return constructor.new(_2097.KlingelnbergCycloPalloidSpiralBevelGearSet)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Hypoid Gear Set') -> '_2095.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'AddKlingelnbergCycloPalloidHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidHypoidGearSet(name if name else None)
        return constructor.new(_2095.KlingelnbergCycloPalloidHypoidGearSet)(method_result) if method_result else None

    def add_straight_bevel_gear_set(self, name: Optional['str'] = 'Straight Bevel Gear Set') -> '_2104.StraightBevelGearSet':
        ''' 'AddStraightBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelGearSet(name if name else None)
        return constructor.new(_2104.StraightBevelGearSet)(method_result) if method_result else None

    def add_hypoid_gear_set(self, name: Optional['str'] = 'Hypoid Gear Set') -> '_2091.HypoidGearSet':
        ''' 'AddHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddHypoidGearSet(name if name else None)
        return constructor.new(_2091.HypoidGearSet)(method_result) if method_result else None

    def add_worm_gear_set(self, name: Optional['str'] = 'Worm Gear Set') -> '_2108.WormGearSet':
        ''' 'AddWormGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddWormGearSet(name if name else None)
        return constructor.new(_2108.WormGearSet)(method_result) if method_result else None

    def add_zerol_bevel_gear_set(self, name: Optional['str'] = 'Zerol Bevel Gear Set') -> '_2110.ZerolBevelGearSet':
        ''' 'AddZerolBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelGearSet(name if name else None)
        return constructor.new(_2110.ZerolBevelGearSet)(method_result) if method_result else None

    def add_clutch(self, name: Optional['str'] = 'Clutch') -> '_2130.Clutch':
        ''' 'AddClutch' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.AddClutch(name if name else None)
        return constructor.new(_2130.Clutch)(method_result) if method_result else None

    def add_synchroniser(self, name: Optional['str'] = 'Synchroniser') -> '_2152.Synchroniser':
        ''' 'AddSynchroniser' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.AddSynchroniser(name if name else None)
        return constructor.new(_2152.Synchroniser)(method_result) if method_result else None

    def add_rolling_ring(self, name: Optional['str'] = 'Rolling Ring') -> '_2147.RollingRing':
        ''' 'AddRollingRing' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.AddRollingRing(name if name else None)
        return constructor.new(_2147.RollingRing)(method_result) if method_result else None

    def add_concept_coupling(self, name: Optional['str'] = 'Concept Coupling') -> '_2133.ConceptCoupling':
        ''' 'AddConceptCoupling' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.AddConceptCoupling(name if name else None)
        return constructor.new(_2133.ConceptCoupling)(method_result) if method_result else None

    def add_cvt(self, name: Optional['str'] = 'CVT') -> '_2137.CVT':
        ''' 'AddCVT' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.AddCVT(name if name else None)
        return constructor.new(_2137.CVT)(method_result) if method_result else None

    def add_spring_damper(self, name: Optional['str'] = 'Spring Damper') -> '_2150.SpringDamper':
        ''' 'AddSpringDamper' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.AddSpringDamper(name if name else None)
        return constructor.new(_2150.SpringDamper)(method_result) if method_result else None

    def add_torque_converter(self, name: Optional['str'] = 'Torque Converter') -> '_2157.TorqueConverter':
        ''' 'AddTorqueConverter' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.AddTorqueConverter(name if name else None)
        return constructor.new(_2157.TorqueConverter)(method_result) if method_result else None

    def add_bolted_joint(self, name: Optional['str'] = 'Bolted Joint') -> '_2003.BoltedJoint':
        ''' 'AddBoltedJoint' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.AddBoltedJoint(name if name else None)
        return constructor.new(_2003.BoltedJoint)(method_result) if method_result else None

    def add_belt_drive_with_options(self, belt_creation_options: Optional['_2124.BeltCreationOptions'] = None) -> '_2128.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            belt_creation_options (mastapy.system_model.part_model.creation_options.BeltCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        method_result = self.wrapped.AddBeltDrive(belt_creation_options.wrapped if belt_creation_options else None)
        return constructor.new(_2128.BeltDrive)(method_result) if method_result else None

    def add_belt_drive(self, centre_distance: Optional['float'] = 0.1, pulley_a_diameter: Optional['float'] = 0.1, pulley_b_diameter: Optional['float'] = 0.1, name: Optional['str'] = 'Belt Drive') -> '_2128.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            centre_distance (float, optional)
            pulley_a_diameter (float, optional)
            pulley_b_diameter (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        centre_distance = float(centre_distance)
        pulley_a_diameter = float(pulley_a_diameter)
        pulley_b_diameter = float(pulley_b_diameter)
        name = str(name)
        method_result = self.wrapped.AddBeltDrive(centre_distance if centre_distance else 0.0, pulley_a_diameter if pulley_a_diameter else 0.0, pulley_b_diameter if pulley_b_diameter else 0.0, name if name else None)
        return constructor.new(_2128.BeltDrive)(method_result) if method_result else None

    def add_planet_carrier_with_options(self, planet_carrier_creation_options: Optional['_2126.PlanetCarrierCreationOptions'] = None) -> '_2027.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            planet_carrier_creation_options (mastapy.system_model.part_model.creation_options.PlanetCarrierCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        method_result = self.wrapped.AddPlanetCarrier(planet_carrier_creation_options.wrapped if planet_carrier_creation_options else None)
        return constructor.new(_2027.PlanetCarrier)(method_result) if method_result else None

    def add_planet_carrier(self, number_of_planets: Optional['int'] = 3, diameter: Optional['float'] = 0.1) -> '_2027.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            number_of_planets (int, optional)
            diameter (float, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        number_of_planets = int(number_of_planets)
        diameter = float(diameter)
        method_result = self.wrapped.AddPlanetCarrier(number_of_planets if number_of_planets else 0, diameter if diameter else 0.0)
        return constructor.new(_2027.PlanetCarrier)(method_result) if method_result else None

    def add_shaft_with_options(self, shaft_creation_options: '_2127.ShaftCreationOptions') -> '_2039.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            shaft_creation_options (mastapy.system_model.part_model.creation_options.ShaftCreationOptions)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        method_result = self.wrapped.AddShaft(shaft_creation_options.wrapped if shaft_creation_options else None)
        return constructor.new(_2039.Shaft)(method_result) if method_result else None

    def add_shaft(self, length: Optional['float'] = 0.1, outer_diameter: Optional['float'] = 0.0, bore: Optional['float'] = 0.0, name: Optional['str'] = 'Shaft') -> '_2039.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            length (float, optional)
            outer_diameter (float, optional)
            bore (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        length = float(length)
        outer_diameter = float(outer_diameter)
        bore = float(bore)
        name = str(name)
        method_result = self.wrapped.AddShaft(length if length else 0.0, outer_diameter if outer_diameter else 0.0, bore if bore else 0.0, name if name else None)
        return constructor.new(_2039.Shaft)(method_result) if method_result else None

    def add_cylindrical_gear_pair_with_options(self, cylindrical_gear_pair_creation_options: Optional['_883.CylindricalGearPairCreationOptions'] = None) -> '_2082.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            cylindrical_gear_pair_creation_options (mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearPair(cylindrical_gear_pair_creation_options.wrapped if cylindrical_gear_pair_creation_options else None)
        return constructor.new(_2082.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_pair(self, centre_distance: 'float') -> '_2082.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            centre_distance (float)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        centre_distance = float(centre_distance)
        method_result = self.wrapped.AddCylindricalGearPair(centre_distance if centre_distance else 0.0)
        return constructor.new(_2082.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set_with_options(self, cylindrical_gear_linear_train_creation_options: Optional['_2125.CylindricalGearLinearTrainCreationOptions'] = None) -> '_2082.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            cylindrical_gear_linear_train_creation_options (mastapy.system_model.part_model.creation_options.CylindricalGearLinearTrainCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearSet(cylindrical_gear_linear_train_creation_options.wrapped if cylindrical_gear_linear_train_creation_options else None)
        return constructor.new(_2082.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set(self, name: 'str', centre_distances: 'List[float]') -> '_2082.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet(name if name else None, centre_distances)
        return constructor.new(_2082.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set_extended(self, name: 'str', normal_pressure_angle: 'float', helix_angle: 'float', normal_module: 'float', pinion_hand: '_135.Hand', centre_distances: 'List[float]') -> '_2082.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            normal_pressure_angle (float)
            helix_angle (float)
            normal_module (float)
            pinion_hand (mastapy.gears.Hand)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        normal_pressure_angle = float(normal_pressure_angle)
        helix_angle = float(helix_angle)
        normal_module = float(normal_module)
        pinion_hand = conversion.mp_to_pn_enum(pinion_hand)
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet(name if name else None, normal_pressure_angle if normal_pressure_angle else 0.0, helix_angle if helix_angle else 0.0, normal_module if normal_module else 0.0, pinion_hand, centre_distances)
        return constructor.new(_2082.CylindricalGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set_with_options(self, spiral_bevel_gear_set_creation_options: Optional['_886.SpiralBevelGearSetCreationOptions'] = None) -> '_2100.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            spiral_bevel_gear_set_creation_options (mastapy.gears.gear_designs.creation_options.SpiralBevelGearSetCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        method_result = self.wrapped.AddSpiralBevelGearSet(spiral_bevel_gear_set_creation_options.wrapped if spiral_bevel_gear_set_creation_options else None)
        return constructor.new(_2100.SpiralBevelGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set_detailed(self, name: Optional['str'] = 'Spiral Bevel Gear Set', outer_transverse_module: Optional['float'] = 0.0, pressure_angle: Optional['float'] = 0.0, mean_spiral_angle: Optional['float'] = 0.5, wheel_number_of_teeth: Optional['int'] = 43, pinion_number_of_teeth: Optional['int'] = 14, wheel_face_width: Optional['float'] = 0.0, pinion_face_width: Optional['float'] = 0.0, pinion_face_width_offset: Optional['float'] = 0.0, shaft_angle: Optional['float'] = 1.6) -> '_2100.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)
            outer_transverse_module (float, optional)
            pressure_angle (float, optional)
            mean_spiral_angle (float, optional)
            wheel_number_of_teeth (int, optional)
            pinion_number_of_teeth (int, optional)
            wheel_face_width (float, optional)
            pinion_face_width (float, optional)
            pinion_face_width_offset (float, optional)
            shaft_angle (float, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        outer_transverse_module = float(outer_transverse_module)
        pressure_angle = float(pressure_angle)
        mean_spiral_angle = float(mean_spiral_angle)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_face_width = float(wheel_face_width)
        pinion_face_width = float(pinion_face_width)
        pinion_face_width_offset = float(pinion_face_width_offset)
        shaft_angle = float(shaft_angle)
        method_result = self.wrapped.AddSpiralBevelGearSet(name if name else None, outer_transverse_module if outer_transverse_module else 0.0, pressure_angle if pressure_angle else 0.0, mean_spiral_angle if mean_spiral_angle else 0.0, wheel_number_of_teeth if wheel_number_of_teeth else 0, pinion_number_of_teeth if pinion_number_of_teeth else 0, wheel_face_width if wheel_face_width else 0.0, pinion_face_width if pinion_face_width else 0.0, pinion_face_width_offset if pinion_face_width_offset else 0.0, shaft_angle if shaft_angle else 0.0)
        return constructor.new(_2100.SpiralBevelGearSet)(method_result) if method_result else None

    def add_hypoid_gear_set_detailed(self, name: Optional['str'] = 'Hypoid Gear Set', pinion_number_of_teeth: Optional['int'] = 7, wheel_number_of_teeth: Optional['int'] = 41, outer_transverse_module: Optional['float'] = 0.0, wheel_face_width: Optional['float'] = 0.1, offset: Optional['float'] = 0.0, average_pressure_angle: Optional['float'] = 0.4, design_method: Optional['_916.AGMAGleasonConicalGearGeometryMethods'] = _916.AGMAGleasonConicalGearGeometryMethods.GLEASON) -> '_2091.HypoidGearSet':
        ''' 'AddHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)
            pinion_number_of_teeth (int, optional)
            wheel_number_of_teeth (int, optional)
            outer_transverse_module (float, optional)
            wheel_face_width (float, optional)
            offset (float, optional)
            average_pressure_angle (float, optional)
            design_method (mastapy.gears.gear_designs.bevel.AGMAGleasonConicalGearGeometryMethods, optional)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        outer_transverse_module = float(outer_transverse_module)
        wheel_face_width = float(wheel_face_width)
        offset = float(offset)
        average_pressure_angle = float(average_pressure_angle)
        design_method = conversion.mp_to_pn_enum(design_method)
        method_result = self.wrapped.AddHypoidGearSet(name if name else None, pinion_number_of_teeth if pinion_number_of_teeth else 0, wheel_number_of_teeth if wheel_number_of_teeth else 0, outer_transverse_module if outer_transverse_module else 0.0, wheel_face_width if wheel_face_width else 0.0, offset if offset else 0.0, average_pressure_angle if average_pressure_angle else 0.0, design_method)
        return constructor.new(_2091.HypoidGearSet)(method_result) if method_result else None

    def add_bearing(self, name: 'str') -> '_2000.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.AddBearing(name if name else None)
        return constructor.new(_2000.Bearing)(method_result) if method_result else None

    def import_fe_mesh_from_file(self, file_name: 'str', stiffness_matrix: '_1390.NodalMatrix') -> '_2016.ImportedFEComponent':
        ''' 'ImportFEMeshFromFile' is the original name of this method.

        Args:
            file_name (str)
            stiffness_matrix (mastapy.nodal_analysis.NodalMatrix)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        file_name = str(file_name)
        method_result = self.wrapped.ImportFEMeshFromFile(file_name if file_name else None, stiffness_matrix.wrapped if stiffness_matrix else None)
        return constructor.new(_2016.ImportedFEComponent)(method_result) if method_result else None

    def all_parts(self) -> 'List[_2026.Part]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Part]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2026.Part.TYPE](), constructor.new(_2026.Part))

    def all_parts_of_type_assembly(self) -> 'List[Assembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Assembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[Assembly.TYPE](), constructor.new(Assembly))

    def all_parts_of_type_abstract_assembly(self) -> 'List[_1996.AbstractAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1996.AbstractAssembly.TYPE](), constructor.new(_1996.AbstractAssembly))

    def all_parts_of_type_abstract_shaft_or_housing(self) -> 'List[_1997.AbstractShaftOrHousing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractShaftOrHousing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1997.AbstractShaftOrHousing.TYPE](), constructor.new(_1997.AbstractShaftOrHousing))

    def all_parts_of_type_bearing(self) -> 'List[_2000.Bearing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bearing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2000.Bearing.TYPE](), constructor.new(_2000.Bearing))

    def all_parts_of_type_bolt(self) -> 'List[_2002.Bolt]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bolt]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2002.Bolt.TYPE](), constructor.new(_2002.Bolt))

    def all_parts_of_type_bolted_joint(self) -> 'List[_2003.BoltedJoint]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.BoltedJoint]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2003.BoltedJoint.TYPE](), constructor.new(_2003.BoltedJoint))

    def all_parts_of_type_component(self) -> 'List[_2004.Component]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Component]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2004.Component.TYPE](), constructor.new(_2004.Component))

    def all_parts_of_type_connector(self) -> 'List[_2007.Connector]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Connector]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2007.Connector.TYPE](), constructor.new(_2007.Connector))

    def all_parts_of_type_datum(self) -> 'List[_2008.Datum]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Datum]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2008.Datum.TYPE](), constructor.new(_2008.Datum))

    def all_parts_of_type_external_cad_model(self) -> 'List[_2011.ExternalCADModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ExternalCADModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2011.ExternalCADModel.TYPE](), constructor.new(_2011.ExternalCADModel))

    def all_parts_of_type_flexible_pin_assembly(self) -> 'List[_2012.FlexiblePinAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.FlexiblePinAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2012.FlexiblePinAssembly.TYPE](), constructor.new(_2012.FlexiblePinAssembly))

    def all_parts_of_type_guide_dxf_model(self) -> 'List[_2013.GuideDxfModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.GuideDxfModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2013.GuideDxfModel.TYPE](), constructor.new(_2013.GuideDxfModel))

    def all_parts_of_type_imported_fe_component(self) -> 'List[_2016.ImportedFEComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ImportedFEComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2016.ImportedFEComponent.TYPE](), constructor.new(_2016.ImportedFEComponent))

    def all_parts_of_type_mass_disc(self) -> 'List[_2020.MassDisc]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MassDisc]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2020.MassDisc.TYPE](), constructor.new(_2020.MassDisc))

    def all_parts_of_type_measurement_component(self) -> 'List[_2021.MeasurementComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MeasurementComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2021.MeasurementComponent.TYPE](), constructor.new(_2021.MeasurementComponent))

    def all_parts_of_type_mountable_component(self) -> 'List[_2022.MountableComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MountableComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2022.MountableComponent.TYPE](), constructor.new(_2022.MountableComponent))

    def all_parts_of_type_oil_seal(self) -> 'List[_2024.OilSeal]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.OilSeal]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2024.OilSeal.TYPE](), constructor.new(_2024.OilSeal))

    def all_parts_of_type_planet_carrier(self) -> 'List[_2027.PlanetCarrier]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PlanetCarrier]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2027.PlanetCarrier.TYPE](), constructor.new(_2027.PlanetCarrier))

    def all_parts_of_type_point_load(self) -> 'List[_2029.PointLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PointLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2029.PointLoad.TYPE](), constructor.new(_2029.PointLoad))

    def all_parts_of_type_power_load(self) -> 'List[_2030.PowerLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PowerLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2030.PowerLoad.TYPE](), constructor.new(_2030.PowerLoad))

    def all_parts_of_type_root_assembly(self) -> 'List[_2032.RootAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.RootAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2032.RootAssembly.TYPE](), constructor.new(_2032.RootAssembly))

    def all_parts_of_type_specialised_assembly(self) -> 'List[_2034.SpecialisedAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.SpecialisedAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2034.SpecialisedAssembly.TYPE](), constructor.new(_2034.SpecialisedAssembly))

    def all_parts_of_type_unbalanced_mass(self) -> 'List[_2035.UnbalancedMass]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.UnbalancedMass]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2035.UnbalancedMass.TYPE](), constructor.new(_2035.UnbalancedMass))

    def all_parts_of_type_virtual_component(self) -> 'List[_2036.VirtualComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.VirtualComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2036.VirtualComponent.TYPE](), constructor.new(_2036.VirtualComponent))

    def all_parts_of_type_shaft(self) -> 'List[_2039.Shaft]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.shaft_model.Shaft]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2039.Shaft.TYPE](), constructor.new(_2039.Shaft))

    def all_parts_of_type_agma_gleason_conical_gear(self) -> 'List[_2069.AGMAGleasonConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2069.AGMAGleasonConicalGear.TYPE](), constructor.new(_2069.AGMAGleasonConicalGear))

    def all_parts_of_type_agma_gleason_conical_gear_set(self) -> 'List[_2070.AGMAGleasonConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2070.AGMAGleasonConicalGearSet.TYPE](), constructor.new(_2070.AGMAGleasonConicalGearSet))

    def all_parts_of_type_bevel_differential_gear(self) -> 'List[_2071.BevelDifferentialGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2071.BevelDifferentialGear.TYPE](), constructor.new(_2071.BevelDifferentialGear))

    def all_parts_of_type_bevel_differential_gear_set(self) -> 'List[_2072.BevelDifferentialGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2072.BevelDifferentialGearSet.TYPE](), constructor.new(_2072.BevelDifferentialGearSet))

    def all_parts_of_type_bevel_differential_planet_gear(self) -> 'List[_2073.BevelDifferentialPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2073.BevelDifferentialPlanetGear.TYPE](), constructor.new(_2073.BevelDifferentialPlanetGear))

    def all_parts_of_type_bevel_differential_sun_gear(self) -> 'List[_2074.BevelDifferentialSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2074.BevelDifferentialSunGear.TYPE](), constructor.new(_2074.BevelDifferentialSunGear))

    def all_parts_of_type_bevel_gear(self) -> 'List[_2075.BevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2075.BevelGear.TYPE](), constructor.new(_2075.BevelGear))

    def all_parts_of_type_bevel_gear_set(self) -> 'List[_2076.BevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2076.BevelGearSet.TYPE](), constructor.new(_2076.BevelGearSet))

    def all_parts_of_type_concept_gear(self) -> 'List[_2077.ConceptGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2077.ConceptGear.TYPE](), constructor.new(_2077.ConceptGear))

    def all_parts_of_type_concept_gear_set(self) -> 'List[_2078.ConceptGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2078.ConceptGearSet.TYPE](), constructor.new(_2078.ConceptGearSet))

    def all_parts_of_type_conical_gear(self) -> 'List[_2079.ConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2079.ConicalGear.TYPE](), constructor.new(_2079.ConicalGear))

    def all_parts_of_type_conical_gear_set(self) -> 'List[_2080.ConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2080.ConicalGearSet.TYPE](), constructor.new(_2080.ConicalGearSet))

    def all_parts_of_type_cylindrical_gear(self) -> 'List[_2081.CylindricalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2081.CylindricalGear.TYPE](), constructor.new(_2081.CylindricalGear))

    def all_parts_of_type_cylindrical_gear_set(self) -> 'List[_2082.CylindricalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2082.CylindricalGearSet.TYPE](), constructor.new(_2082.CylindricalGearSet))

    def all_parts_of_type_cylindrical_planet_gear(self) -> 'List[_2083.CylindricalPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2083.CylindricalPlanetGear.TYPE](), constructor.new(_2083.CylindricalPlanetGear))

    def all_parts_of_type_face_gear(self) -> 'List[_2084.FaceGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2084.FaceGear.TYPE](), constructor.new(_2084.FaceGear))

    def all_parts_of_type_face_gear_set(self) -> 'List[_2085.FaceGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2085.FaceGearSet.TYPE](), constructor.new(_2085.FaceGearSet))

    def all_parts_of_type_gear(self) -> 'List[_2086.Gear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.Gear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2086.Gear.TYPE](), constructor.new(_2086.Gear))

    def all_parts_of_type_gear_set(self) -> 'List[_2088.GearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.GearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2088.GearSet.TYPE](), constructor.new(_2088.GearSet))

    def all_parts_of_type_hypoid_gear(self) -> 'List[_2090.HypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2090.HypoidGear.TYPE](), constructor.new(_2090.HypoidGear))

    def all_parts_of_type_hypoid_gear_set(self) -> 'List[_2091.HypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2091.HypoidGearSet.TYPE](), constructor.new(_2091.HypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> 'List[_2092.KlingelnbergCycloPalloidConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2092.KlingelnbergCycloPalloidConicalGear.TYPE](), constructor.new(_2092.KlingelnbergCycloPalloidConicalGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> 'List[_2093.KlingelnbergCycloPalloidConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2093.KlingelnbergCycloPalloidConicalGearSet.TYPE](), constructor.new(_2093.KlingelnbergCycloPalloidConicalGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> 'List[_2094.KlingelnbergCycloPalloidHypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2094.KlingelnbergCycloPalloidHypoidGear.TYPE](), constructor.new(_2094.KlingelnbergCycloPalloidHypoidGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> 'List[_2095.KlingelnbergCycloPalloidHypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2095.KlingelnbergCycloPalloidHypoidGearSet.TYPE](), constructor.new(_2095.KlingelnbergCycloPalloidHypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> 'List[_2096.KlingelnbergCycloPalloidSpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2096.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](), constructor.new(_2096.KlingelnbergCycloPalloidSpiralBevelGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> 'List[_2097.KlingelnbergCycloPalloidSpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2097.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](), constructor.new(_2097.KlingelnbergCycloPalloidSpiralBevelGearSet))

    def all_parts_of_type_planetary_gear_set(self) -> 'List[_2098.PlanetaryGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.PlanetaryGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2098.PlanetaryGearSet.TYPE](), constructor.new(_2098.PlanetaryGearSet))

    def all_parts_of_type_spiral_bevel_gear(self) -> 'List[_2099.SpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2099.SpiralBevelGear.TYPE](), constructor.new(_2099.SpiralBevelGear))

    def all_parts_of_type_spiral_bevel_gear_set(self) -> 'List[_2100.SpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2100.SpiralBevelGearSet.TYPE](), constructor.new(_2100.SpiralBevelGearSet))

    def all_parts_of_type_straight_bevel_diff_gear(self) -> 'List[_2101.StraightBevelDiffGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2101.StraightBevelDiffGear.TYPE](), constructor.new(_2101.StraightBevelDiffGear))

    def all_parts_of_type_straight_bevel_diff_gear_set(self) -> 'List[_2102.StraightBevelDiffGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2102.StraightBevelDiffGearSet.TYPE](), constructor.new(_2102.StraightBevelDiffGearSet))

    def all_parts_of_type_straight_bevel_gear(self) -> 'List[_2103.StraightBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2103.StraightBevelGear.TYPE](), constructor.new(_2103.StraightBevelGear))

    def all_parts_of_type_straight_bevel_gear_set(self) -> 'List[_2104.StraightBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2104.StraightBevelGearSet.TYPE](), constructor.new(_2104.StraightBevelGearSet))

    def all_parts_of_type_straight_bevel_planet_gear(self) -> 'List[_2105.StraightBevelPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2105.StraightBevelPlanetGear.TYPE](), constructor.new(_2105.StraightBevelPlanetGear))

    def all_parts_of_type_straight_bevel_sun_gear(self) -> 'List[_2106.StraightBevelSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2106.StraightBevelSunGear.TYPE](), constructor.new(_2106.StraightBevelSunGear))

    def all_parts_of_type_worm_gear(self) -> 'List[_2107.WormGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2107.WormGear.TYPE](), constructor.new(_2107.WormGear))

    def all_parts_of_type_worm_gear_set(self) -> 'List[_2108.WormGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2108.WormGearSet.TYPE](), constructor.new(_2108.WormGearSet))

    def all_parts_of_type_zerol_bevel_gear(self) -> 'List[_2109.ZerolBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2109.ZerolBevelGear.TYPE](), constructor.new(_2109.ZerolBevelGear))

    def all_parts_of_type_zerol_bevel_gear_set(self) -> 'List[_2110.ZerolBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2110.ZerolBevelGearSet.TYPE](), constructor.new(_2110.ZerolBevelGearSet))

    def all_parts_of_type_belt_drive(self) -> 'List[_2128.BeltDrive]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.BeltDrive]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2128.BeltDrive.TYPE](), constructor.new(_2128.BeltDrive))

    def all_parts_of_type_clutch(self) -> 'List[_2130.Clutch]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Clutch]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2130.Clutch.TYPE](), constructor.new(_2130.Clutch))

    def all_parts_of_type_clutch_half(self) -> 'List[_2131.ClutchHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ClutchHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2131.ClutchHalf.TYPE](), constructor.new(_2131.ClutchHalf))

    def all_parts_of_type_concept_coupling(self) -> 'List[_2133.ConceptCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2133.ConceptCoupling.TYPE](), constructor.new(_2133.ConceptCoupling))

    def all_parts_of_type_concept_coupling_half(self) -> 'List[_2134.ConceptCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2134.ConceptCouplingHalf.TYPE](), constructor.new(_2134.ConceptCouplingHalf))

    def all_parts_of_type_coupling(self) -> 'List[_2135.Coupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Coupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2135.Coupling.TYPE](), constructor.new(_2135.Coupling))

    def all_parts_of_type_coupling_half(self) -> 'List[_2136.CouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2136.CouplingHalf.TYPE](), constructor.new(_2136.CouplingHalf))

    def all_parts_of_type_cvt(self) -> 'List[_2137.CVT]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVT]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2137.CVT.TYPE](), constructor.new(_2137.CVT))

    def all_parts_of_type_cvt_pulley(self) -> 'List[_2138.CVTPulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVTPulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2138.CVTPulley.TYPE](), constructor.new(_2138.CVTPulley))

    def all_parts_of_type_part_to_part_shear_coupling(self) -> 'List[_2139.PartToPartShearCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2139.PartToPartShearCoupling.TYPE](), constructor.new(_2139.PartToPartShearCoupling))

    def all_parts_of_type_part_to_part_shear_coupling_half(self) -> 'List[_2140.PartToPartShearCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2140.PartToPartShearCouplingHalf.TYPE](), constructor.new(_2140.PartToPartShearCouplingHalf))

    def all_parts_of_type_pulley(self) -> 'List[_2141.Pulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Pulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2141.Pulley.TYPE](), constructor.new(_2141.Pulley))

    def all_parts_of_type_rolling_ring(self) -> 'List[_2147.RollingRing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2147.RollingRing.TYPE](), constructor.new(_2147.RollingRing))

    def all_parts_of_type_rolling_ring_assembly(self) -> 'List[_2148.RollingRingAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRingAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2148.RollingRingAssembly.TYPE](), constructor.new(_2148.RollingRingAssembly))

    def all_parts_of_type_shaft_hub_connection(self) -> 'List[_2149.ShaftHubConnection]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ShaftHubConnection]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2149.ShaftHubConnection.TYPE](), constructor.new(_2149.ShaftHubConnection))

    def all_parts_of_type_spring_damper(self) -> 'List[_2150.SpringDamper]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamper]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2150.SpringDamper.TYPE](), constructor.new(_2150.SpringDamper))

    def all_parts_of_type_spring_damper_half(self) -> 'List[_2151.SpringDamperHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamperHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2151.SpringDamperHalf.TYPE](), constructor.new(_2151.SpringDamperHalf))

    def all_parts_of_type_synchroniser(self) -> 'List[_2152.Synchroniser]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Synchroniser]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2152.Synchroniser.TYPE](), constructor.new(_2152.Synchroniser))

    def all_parts_of_type_synchroniser_half(self) -> 'List[_2154.SynchroniserHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2154.SynchroniserHalf.TYPE](), constructor.new(_2154.SynchroniserHalf))

    def all_parts_of_type_synchroniser_part(self) -> 'List[_2155.SynchroniserPart]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserPart]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2155.SynchroniserPart.TYPE](), constructor.new(_2155.SynchroniserPart))

    def all_parts_of_type_synchroniser_sleeve(self) -> 'List[_2156.SynchroniserSleeve]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserSleeve]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2156.SynchroniserSleeve.TYPE](), constructor.new(_2156.SynchroniserSleeve))

    def all_parts_of_type_torque_converter(self) -> 'List[_2157.TorqueConverter]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverter]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2157.TorqueConverter.TYPE](), constructor.new(_2157.TorqueConverter))

    def all_parts_of_type_torque_converter_pump(self) -> 'List[_2158.TorqueConverterPump]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterPump]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2158.TorqueConverterPump.TYPE](), constructor.new(_2158.TorqueConverterPump))

    def all_parts_of_type_torque_converter_turbine(self) -> 'List[_2160.TorqueConverterTurbine]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterTurbine]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2160.TorqueConverterTurbine.TYPE](), constructor.new(_2160.TorqueConverterTurbine))

    def add_axial_clearance_bearing(self, name: 'str', contact_diameter: 'float') -> '_2000.Bearing':
        ''' 'AddAxialClearanceBearing' is the original name of this method.

        Args:
            name (str)
            contact_diameter (float)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        contact_diameter = float(contact_diameter)
        method_result = self.wrapped.AddAxialClearanceBearing(name if name else None, contact_diameter if contact_diameter else 0.0)
        return constructor.new(_2000.Bearing)(method_result) if method_result else None

    def add_shaft_hub_connection(self, name: 'str') -> '_2149.ShaftHubConnection':
        ''' 'AddShaftHubConnection' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.AddShaftHubConnection(name if name else None)
        return constructor.new(_2149.ShaftHubConnection)(method_result) if method_result else None

    def add_rolling_bearing_from_catalogue(self, catalogue: '_1509.BearingCatalog', designation: 'str', name: 'str') -> '_2000.Bearing':
        ''' 'AddRollingBearingFromCatalogue' is the original name of this method.

        Args:
            catalogue (mastapy.bearings.BearingCatalog)
            designation (str)
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        catalogue = conversion.mp_to_pn_enum(catalogue)
        designation = str(designation)
        name = str(name)
        method_result = self.wrapped.AddRollingBearingFromCatalogue(catalogue, designation if designation else None, name if name else None)
        return constructor.new(_2000.Bearing)(method_result) if method_result else None

    def add_bearing_with_name_and_rolling_bearing_type(self, name: 'str', type_: '_1534.RollingBearingType') -> '_2000.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        method_result = self.wrapped.AddBearing(name if name else None, type_)
        return constructor.new(_2000.Bearing)(method_result) if method_result else None

    def add_bearing_with_name_rolling_bearing_type_and_designation(self, name: 'str', type_: '_1534.RollingBearingType', designation: 'str') -> '_2000.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)
            designation (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        designation = str(designation)
        method_result = self.wrapped.AddBearing(name if name else None, type_, designation if designation else None)
        return constructor.new(_2000.Bearing)(method_result) if method_result else None
