﻿'''_1307.py

OptimizationVariable
'''


from typing import List

from mastapy.utility.units_and_measurements import _1360
from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements.measurements import (
    _1367, _1368, _1369, _1370,
    _1371, _1372, _1373, _1374,
    _1375, _1376, _1377, _1378,
    _1379, _1380, _1381, _1382,
    _1383, _1384, _1385, _1386,
    _1387, _1388, _1389, _1390,
    _1391, _1392, _1393, _1394,
    _1395, _1396, _1397, _1398,
    _1399, _1400, _1401, _1402,
    _1403, _1404, _1405, _1406,
    _1407, _1408, _1409, _1410,
    _1411, _1412, _1413, _1414,
    _1415, _1416, _1417, _1418,
    _1419, _1420, _1421, _1422,
    _1423, _1424, _1425, _1426,
    _1427, _1428, _1429, _1430,
    _1431, _1432, _1433, _1434,
    _1435, _1436, _1437, _1438,
    _1439, _1440, _1441, _1442,
    _1443, _1444, _1445, _1446,
    _1447, _1448, _1449, _1450,
    _1451, _1452, _1453, _1454,
    _1455, _1456, _1457, _1458,
    _1459, _1460, _1461, _1462,
    _1463, _1464, _1465, _1466,
    _1467, _1468, _1469, _1470,
    _1471, _1472, _1473, _1474
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_VARIABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'OptimizationVariable')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationVariable',)


class OptimizationVariable(_0.APIBase):
    '''OptimizationVariable

    This is a mastapy class.
    '''

    TYPE = _OPTIMIZATION_VARIABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimizationVariable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def measurement(self) -> '_1360.MeasurementBase':
        '''MeasurementBase: 'Measurement' is the original name of this property.'''

        if _1360.MeasurementBase.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MeasurementBase. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement.setter
    def measurement(self, value: '_1360.MeasurementBase'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_acceleration(self) -> '_1367.Acceleration':
        '''Acceleration: 'Measurement' is the original name of this property.'''

        if _1367.Acceleration.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Acceleration. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_acceleration.setter
    def measurement_of_type_acceleration(self, value: '_1367.Acceleration'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle(self) -> '_1368.Angle':
        '''Angle: 'Measurement' is the original name of this property.'''

        if _1368.Angle.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Angle. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angle.setter
    def measurement_of_type_angle(self, value: '_1368.Angle'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle_per_unit_temperature(self) -> '_1369.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'Measurement' is the original name of this property.'''

        if _1369.AnglePerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AnglePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angle_per_unit_temperature.setter
    def measurement_of_type_angle_per_unit_temperature(self, value: '_1369.AnglePerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle_small(self) -> '_1370.AngleSmall':
        '''AngleSmall: 'Measurement' is the original name of this property.'''

        if _1370.AngleSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngleSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angle_small.setter
    def measurement_of_type_angle_small(self, value: '_1370.AngleSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angle_very_small(self) -> '_1371.AngleVerySmall':
        '''AngleVerySmall: 'Measurement' is the original name of this property.'''

        if _1371.AngleVerySmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngleVerySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angle_very_small.setter
    def measurement_of_type_angle_very_small(self, value: '_1371.AngleVerySmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_acceleration(self) -> '_1372.AngularAcceleration':
        '''AngularAcceleration: 'Measurement' is the original name of this property.'''

        if _1372.AngularAcceleration.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularAcceleration. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angular_acceleration.setter
    def measurement_of_type_angular_acceleration(self, value: '_1372.AngularAcceleration'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_compliance(self) -> '_1373.AngularCompliance':
        '''AngularCompliance: 'Measurement' is the original name of this property.'''

        if _1373.AngularCompliance.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularCompliance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angular_compliance.setter
    def measurement_of_type_angular_compliance(self, value: '_1373.AngularCompliance'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_jerk(self) -> '_1374.AngularJerk':
        '''AngularJerk: 'Measurement' is the original name of this property.'''

        if _1374.AngularJerk.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularJerk. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angular_jerk.setter
    def measurement_of_type_angular_jerk(self, value: '_1374.AngularJerk'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_stiffness(self) -> '_1375.AngularStiffness':
        '''AngularStiffness: 'Measurement' is the original name of this property.'''

        if _1375.AngularStiffness.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularStiffness. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angular_stiffness.setter
    def measurement_of_type_angular_stiffness(self, value: '_1375.AngularStiffness'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_angular_velocity(self) -> '_1376.AngularVelocity':
        '''AngularVelocity: 'Measurement' is the original name of this property.'''

        if _1376.AngularVelocity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularVelocity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_angular_velocity.setter
    def measurement_of_type_angular_velocity(self, value: '_1376.AngularVelocity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_area(self) -> '_1377.Area':
        '''Area: 'Measurement' is the original name of this property.'''

        if _1377.Area.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Area. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_area.setter
    def measurement_of_type_area(self, value: '_1377.Area'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_area_small(self) -> '_1378.AreaSmall':
        '''AreaSmall: 'Measurement' is the original name of this property.'''

        if _1378.AreaSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AreaSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_area_small.setter
    def measurement_of_type_area_small(self, value: '_1378.AreaSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_cycles(self) -> '_1379.Cycles':
        '''Cycles: 'Measurement' is the original name of this property.'''

        if _1379.Cycles.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Cycles. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_cycles.setter
    def measurement_of_type_cycles(self, value: '_1379.Cycles'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_damage(self) -> '_1380.Damage':
        '''Damage: 'Measurement' is the original name of this property.'''

        if _1380.Damage.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Damage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_damage.setter
    def measurement_of_type_damage(self, value: '_1380.Damage'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_damage_rate(self) -> '_1381.DamageRate':
        '''DamageRate: 'Measurement' is the original name of this property.'''

        if _1381.DamageRate.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to DamageRate. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_damage_rate.setter
    def measurement_of_type_damage_rate(self, value: '_1381.DamageRate'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_data_size(self) -> '_1382.DataSize':
        '''DataSize: 'Measurement' is the original name of this property.'''

        if _1382.DataSize.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to DataSize. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_data_size.setter
    def measurement_of_type_data_size(self, value: '_1382.DataSize'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_decibel(self) -> '_1383.Decibel':
        '''Decibel: 'Measurement' is the original name of this property.'''

        if _1383.Decibel.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Decibel. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_decibel.setter
    def measurement_of_type_decibel(self, value: '_1383.Decibel'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_density(self) -> '_1384.Density':
        '''Density: 'Measurement' is the original name of this property.'''

        if _1384.Density.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Density. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_density.setter
    def measurement_of_type_density(self, value: '_1384.Density'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy(self) -> '_1385.Energy':
        '''Energy: 'Measurement' is the original name of this property.'''

        if _1385.Energy.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Energy. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_energy.setter
    def measurement_of_type_energy(self, value: '_1385.Energy'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy_per_unit_area(self) -> '_1386.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'Measurement' is the original name of this property.'''

        if _1386.EnergyPerUnitArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergyPerUnitArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_energy_per_unit_area.setter
    def measurement_of_type_energy_per_unit_area(self, value: '_1386.EnergyPerUnitArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy_per_unit_area_small(self) -> '_1387.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'Measurement' is the original name of this property.'''

        if _1387.EnergyPerUnitAreaSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_energy_per_unit_area_small.setter
    def measurement_of_type_energy_per_unit_area_small(self, value: '_1387.EnergyPerUnitAreaSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_energy_small(self) -> '_1388.EnergySmall':
        '''EnergySmall: 'Measurement' is the original name of this property.'''

        if _1388.EnergySmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_energy_small.setter
    def measurement_of_type_energy_small(self, value: '_1388.EnergySmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_enum(self) -> '_1389.Enum':
        '''Enum: 'Measurement' is the original name of this property.'''

        if _1389.Enum.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Enum. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_enum.setter
    def measurement_of_type_enum(self, value: '_1389.Enum'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_flow_rate(self) -> '_1390.FlowRate':
        '''FlowRate: 'Measurement' is the original name of this property.'''

        if _1390.FlowRate.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FlowRate. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_flow_rate.setter
    def measurement_of_type_flow_rate(self, value: '_1390.FlowRate'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force(self) -> '_1391.Force':
        '''Force: 'Measurement' is the original name of this property.'''

        if _1391.Force.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Force. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_force.setter
    def measurement_of_type_force(self, value: '_1391.Force'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force_per_unit_length(self) -> '_1392.ForcePerUnitLength':
        '''ForcePerUnitLength: 'Measurement' is the original name of this property.'''

        if _1392.ForcePerUnitLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_force_per_unit_length.setter
    def measurement_of_type_force_per_unit_length(self, value: '_1392.ForcePerUnitLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force_per_unit_pressure(self) -> '_1393.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'Measurement' is the original name of this property.'''

        if _1393.ForcePerUnitPressure.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitPressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_force_per_unit_pressure.setter
    def measurement_of_type_force_per_unit_pressure(self, value: '_1393.ForcePerUnitPressure'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_force_per_unit_temperature(self) -> '_1394.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'Measurement' is the original name of this property.'''

        if _1394.ForcePerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_force_per_unit_temperature.setter
    def measurement_of_type_force_per_unit_temperature(self, value: '_1394.ForcePerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_fraction_measurement_base(self) -> '_1395.FractionMeasurementBase':
        '''FractionMeasurementBase: 'Measurement' is the original name of this property.'''

        if _1395.FractionMeasurementBase.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FractionMeasurementBase. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_fraction_measurement_base.setter
    def measurement_of_type_fraction_measurement_base(self, value: '_1395.FractionMeasurementBase'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_frequency(self) -> '_1396.Frequency':
        '''Frequency: 'Measurement' is the original name of this property.'''

        if _1396.Frequency.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Frequency. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_frequency.setter
    def measurement_of_type_frequency(self, value: '_1396.Frequency'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_fuel_consumption_engine(self) -> '_1397.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'Measurement' is the original name of this property.'''

        if _1397.FuelConsumptionEngine.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FuelConsumptionEngine. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_fuel_consumption_engine.setter
    def measurement_of_type_fuel_consumption_engine(self, value: '_1397.FuelConsumptionEngine'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_fuel_efficiency_vehicle(self) -> '_1398.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'Measurement' is the original name of this property.'''

        if _1398.FuelEfficiencyVehicle.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FuelEfficiencyVehicle. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_fuel_efficiency_vehicle.setter
    def measurement_of_type_fuel_efficiency_vehicle(self, value: '_1398.FuelEfficiencyVehicle'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_gradient(self) -> '_1399.Gradient':
        '''Gradient: 'Measurement' is the original name of this property.'''

        if _1399.Gradient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Gradient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_gradient.setter
    def measurement_of_type_gradient(self, value: '_1399.Gradient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_conductivity(self) -> '_1400.HeatConductivity':
        '''HeatConductivity: 'Measurement' is the original name of this property.'''

        if _1400.HeatConductivity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatConductivity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_heat_conductivity.setter
    def measurement_of_type_heat_conductivity(self, value: '_1400.HeatConductivity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_transfer(self) -> '_1401.HeatTransfer':
        '''HeatTransfer: 'Measurement' is the original name of this property.'''

        if _1401.HeatTransfer.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransfer. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_heat_transfer.setter
    def measurement_of_type_heat_transfer(self, value: '_1401.HeatTransfer'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1402.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'Measurement' is the original name of this property.'''

        if _1402.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth.setter
    def measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self, value: '_1402.HeatTransferCoefficientForPlasticGearTooth'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_heat_transfer_resistance(self) -> '_1403.HeatTransferResistance':
        '''HeatTransferResistance: 'Measurement' is the original name of this property.'''

        if _1403.HeatTransferResistance.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransferResistance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_heat_transfer_resistance.setter
    def measurement_of_type_heat_transfer_resistance(self, value: '_1403.HeatTransferResistance'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_impulse(self) -> '_1404.Impulse':
        '''Impulse: 'Measurement' is the original name of this property.'''

        if _1404.Impulse.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Impulse. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_impulse.setter
    def measurement_of_type_impulse(self, value: '_1404.Impulse'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_index(self) -> '_1405.Index':
        '''Index: 'Measurement' is the original name of this property.'''

        if _1405.Index.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Index. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_index.setter
    def measurement_of_type_index(self, value: '_1405.Index'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_integer(self) -> '_1406.Integer':
        '''Integer: 'Measurement' is the original name of this property.'''

        if _1406.Integer.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Integer. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_integer.setter
    def measurement_of_type_integer(self, value: '_1406.Integer'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_inverse_short_length(self) -> '_1407.InverseShortLength':
        '''InverseShortLength: 'Measurement' is the original name of this property.'''

        if _1407.InverseShortLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to InverseShortLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_inverse_short_length.setter
    def measurement_of_type_inverse_short_length(self, value: '_1407.InverseShortLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_inverse_short_time(self) -> '_1408.InverseShortTime':
        '''InverseShortTime: 'Measurement' is the original name of this property.'''

        if _1408.InverseShortTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to InverseShortTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_inverse_short_time.setter
    def measurement_of_type_inverse_short_time(self, value: '_1408.InverseShortTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_jerk(self) -> '_1409.Jerk':
        '''Jerk: 'Measurement' is the original name of this property.'''

        if _1409.Jerk.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Jerk. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_jerk.setter
    def measurement_of_type_jerk(self, value: '_1409.Jerk'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_kinematic_viscosity(self) -> '_1410.KinematicViscosity':
        '''KinematicViscosity: 'Measurement' is the original name of this property.'''

        if _1410.KinematicViscosity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to KinematicViscosity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_kinematic_viscosity.setter
    def measurement_of_type_kinematic_viscosity(self, value: '_1410.KinematicViscosity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_long(self) -> '_1411.LengthLong':
        '''LengthLong: 'Measurement' is the original name of this property.'''

        if _1411.LengthLong.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthLong. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_long.setter
    def measurement_of_type_length_long(self, value: '_1411.LengthLong'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_medium(self) -> '_1412.LengthMedium':
        '''LengthMedium: 'Measurement' is the original name of this property.'''

        if _1412.LengthMedium.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthMedium. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_medium.setter
    def measurement_of_type_length_medium(self, value: '_1412.LengthMedium'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_per_unit_temperature(self) -> '_1413.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'Measurement' is the original name of this property.'''

        if _1413.LengthPerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthPerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_per_unit_temperature.setter
    def measurement_of_type_length_per_unit_temperature(self, value: '_1413.LengthPerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_short(self) -> '_1414.LengthShort':
        '''LengthShort: 'Measurement' is the original name of this property.'''

        if _1414.LengthShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_short.setter
    def measurement_of_type_length_short(self, value: '_1414.LengthShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_to_the_fourth(self) -> '_1415.LengthToTheFourth':
        '''LengthToTheFourth: 'Measurement' is the original name of this property.'''

        if _1415.LengthToTheFourth.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthToTheFourth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_to_the_fourth.setter
    def measurement_of_type_length_to_the_fourth(self, value: '_1415.LengthToTheFourth'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_very_long(self) -> '_1416.LengthVeryLong':
        '''LengthVeryLong: 'Measurement' is the original name of this property.'''

        if _1416.LengthVeryLong.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryLong. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_very_long.setter
    def measurement_of_type_length_very_long(self, value: '_1416.LengthVeryLong'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_very_short(self) -> '_1417.LengthVeryShort':
        '''LengthVeryShort: 'Measurement' is the original name of this property.'''

        if _1417.LengthVeryShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_very_short.setter
    def measurement_of_type_length_very_short(self, value: '_1417.LengthVeryShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_length_very_short_per_length_short(self) -> '_1418.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'Measurement' is the original name of this property.'''

        if _1418.LengthVeryShortPerLengthShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_length_very_short_per_length_short.setter
    def measurement_of_type_length_very_short_per_length_short(self, value: '_1418.LengthVeryShortPerLengthShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_angular_damping(self) -> '_1419.LinearAngularDamping':
        '''LinearAngularDamping: 'Measurement' is the original name of this property.'''

        if _1419.LinearAngularDamping.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearAngularDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_linear_angular_damping.setter
    def measurement_of_type_linear_angular_damping(self, value: '_1419.LinearAngularDamping'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_angular_stiffness_cross_term(self) -> '_1420.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'Measurement' is the original name of this property.'''

        if _1420.LinearAngularStiffnessCrossTerm.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_linear_angular_stiffness_cross_term.setter
    def measurement_of_type_linear_angular_stiffness_cross_term(self, value: '_1420.LinearAngularStiffnessCrossTerm'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_damping(self) -> '_1421.LinearDamping':
        '''LinearDamping: 'Measurement' is the original name of this property.'''

        if _1421.LinearDamping.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_linear_damping.setter
    def measurement_of_type_linear_damping(self, value: '_1421.LinearDamping'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_flexibility(self) -> '_1422.LinearFlexibility':
        '''LinearFlexibility: 'Measurement' is the original name of this property.'''

        if _1422.LinearFlexibility.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearFlexibility. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_linear_flexibility.setter
    def measurement_of_type_linear_flexibility(self, value: '_1422.LinearFlexibility'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_linear_stiffness(self) -> '_1423.LinearStiffness':
        '''LinearStiffness: 'Measurement' is the original name of this property.'''

        if _1423.LinearStiffness.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearStiffness. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_linear_stiffness.setter
    def measurement_of_type_linear_stiffness(self, value: '_1423.LinearStiffness'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_mass(self) -> '_1424.Mass':
        '''Mass: 'Measurement' is the original name of this property.'''

        if _1424.Mass.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Mass. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_mass.setter
    def measurement_of_type_mass(self, value: '_1424.Mass'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_mass_per_unit_length(self) -> '_1425.MassPerUnitLength':
        '''MassPerUnitLength: 'Measurement' is the original name of this property.'''

        if _1425.MassPerUnitLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MassPerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_mass_per_unit_length.setter
    def measurement_of_type_mass_per_unit_length(self, value: '_1425.MassPerUnitLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_mass_per_unit_time(self) -> '_1426.MassPerUnitTime':
        '''MassPerUnitTime: 'Measurement' is the original name of this property.'''

        if _1426.MassPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MassPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_mass_per_unit_time.setter
    def measurement_of_type_mass_per_unit_time(self, value: '_1426.MassPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_moment_of_inertia(self) -> '_1427.MomentOfInertia':
        '''MomentOfInertia: 'Measurement' is the original name of this property.'''

        if _1427.MomentOfInertia.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentOfInertia. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_moment_of_inertia.setter
    def measurement_of_type_moment_of_inertia(self, value: '_1427.MomentOfInertia'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_moment_of_inertia_per_unit_length(self) -> '_1428.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'Measurement' is the original name of this property.'''

        if _1428.MomentOfInertiaPerUnitLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_moment_of_inertia_per_unit_length.setter
    def measurement_of_type_moment_of_inertia_per_unit_length(self, value: '_1428.MomentOfInertiaPerUnitLength'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_moment_per_unit_pressure(self) -> '_1429.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'Measurement' is the original name of this property.'''

        if _1429.MomentPerUnitPressure.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentPerUnitPressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_moment_per_unit_pressure.setter
    def measurement_of_type_moment_per_unit_pressure(self, value: '_1429.MomentPerUnitPressure'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_number(self) -> '_1430.Number':
        '''Number: 'Measurement' is the original name of this property.'''

        if _1430.Number.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Number. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_number.setter
    def measurement_of_type_number(self, value: '_1430.Number'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_percentage(self) -> '_1431.Percentage':
        '''Percentage: 'Measurement' is the original name of this property.'''

        if _1431.Percentage.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Percentage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_percentage.setter
    def measurement_of_type_percentage(self, value: '_1431.Percentage'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power(self) -> '_1432.Power':
        '''Power: 'Measurement' is the original name of this property.'''

        if _1432.Power.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Power. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_power.setter
    def measurement_of_type_power(self, value: '_1432.Power'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_per_small_area(self) -> '_1433.PowerPerSmallArea':
        '''PowerPerSmallArea: 'Measurement' is the original name of this property.'''

        if _1433.PowerPerSmallArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerPerSmallArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_power_per_small_area.setter
    def measurement_of_type_power_per_small_area(self, value: '_1433.PowerPerSmallArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_per_unit_time(self) -> '_1434.PowerPerUnitTime':
        '''PowerPerUnitTime: 'Measurement' is the original name of this property.'''

        if _1434.PowerPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_power_per_unit_time.setter
    def measurement_of_type_power_per_unit_time(self, value: '_1434.PowerPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small(self) -> '_1435.PowerSmall':
        '''PowerSmall: 'Measurement' is the original name of this property.'''

        if _1435.PowerSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_power_small.setter
    def measurement_of_type_power_small(self, value: '_1435.PowerSmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small_per_area(self) -> '_1436.PowerSmallPerArea':
        '''PowerSmallPerArea: 'Measurement' is the original name of this property.'''

        if _1436.PowerSmallPerArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_power_small_per_area.setter
    def measurement_of_type_power_small_per_area(self, value: '_1436.PowerSmallPerArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1437.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'Measurement' is the original name of this property.'''

        if _1437.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_power_small_per_unit_area_per_unit_time.setter
    def measurement_of_type_power_small_per_unit_area_per_unit_time(self, value: '_1437.PowerSmallPerUnitAreaPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_power_small_per_unit_time(self) -> '_1438.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'Measurement' is the original name of this property.'''

        if _1438.PowerSmallPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_power_small_per_unit_time.setter
    def measurement_of_type_power_small_per_unit_time(self, value: '_1438.PowerSmallPerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure(self) -> '_1439.Pressure':
        '''Pressure: 'Measurement' is the original name of this property.'''

        if _1439.Pressure.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Pressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_pressure.setter
    def measurement_of_type_pressure(self, value: '_1439.Pressure'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure_per_unit_time(self) -> '_1440.PressurePerUnitTime':
        '''PressurePerUnitTime: 'Measurement' is the original name of this property.'''

        if _1440.PressurePerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressurePerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_pressure_per_unit_time.setter
    def measurement_of_type_pressure_per_unit_time(self, value: '_1440.PressurePerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure_velocity_product(self) -> '_1441.PressureVelocityProduct':
        '''PressureVelocityProduct: 'Measurement' is the original name of this property.'''

        if _1441.PressureVelocityProduct.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressureVelocityProduct. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_pressure_velocity_product.setter
    def measurement_of_type_pressure_velocity_product(self, value: '_1441.PressureVelocityProduct'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_pressure_viscosity_coefficient(self) -> '_1442.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'Measurement' is the original name of this property.'''

        if _1442.PressureViscosityCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressureViscosityCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_pressure_viscosity_coefficient.setter
    def measurement_of_type_pressure_viscosity_coefficient(self, value: '_1442.PressureViscosityCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_price(self) -> '_1443.Price':
        '''Price: 'Measurement' is the original name of this property.'''

        if _1443.Price.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Price. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_price.setter
    def measurement_of_type_price(self, value: '_1443.Price'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_quadratic_angular_damping(self) -> '_1444.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'Measurement' is the original name of this property.'''

        if _1444.QuadraticAngularDamping.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to QuadraticAngularDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_quadratic_angular_damping.setter
    def measurement_of_type_quadratic_angular_damping(self, value: '_1444.QuadraticAngularDamping'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_quadratic_drag(self) -> '_1445.QuadraticDrag':
        '''QuadraticDrag: 'Measurement' is the original name of this property.'''

        if _1445.QuadraticDrag.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to QuadraticDrag. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_quadratic_drag.setter
    def measurement_of_type_quadratic_drag(self, value: '_1445.QuadraticDrag'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_rescaled_measurement(self) -> '_1446.RescaledMeasurement':
        '''RescaledMeasurement: 'Measurement' is the original name of this property.'''

        if _1446.RescaledMeasurement.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to RescaledMeasurement. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_rescaled_measurement.setter
    def measurement_of_type_rescaled_measurement(self, value: '_1446.RescaledMeasurement'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_rotatum(self) -> '_1447.Rotatum':
        '''Rotatum: 'Measurement' is the original name of this property.'''

        if _1447.Rotatum.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Rotatum. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_rotatum.setter
    def measurement_of_type_rotatum(self, value: '_1447.Rotatum'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_safety_factor(self) -> '_1448.SafetyFactor':
        '''SafetyFactor: 'Measurement' is the original name of this property.'''

        if _1448.SafetyFactor.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SafetyFactor. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_safety_factor.setter
    def measurement_of_type_safety_factor(self, value: '_1448.SafetyFactor'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_specific_acoustic_impedance(self) -> '_1449.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'Measurement' is the original name of this property.'''

        if _1449.SpecificAcousticImpedance.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SpecificAcousticImpedance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_specific_acoustic_impedance.setter
    def measurement_of_type_specific_acoustic_impedance(self, value: '_1449.SpecificAcousticImpedance'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_specific_heat(self) -> '_1450.SpecificHeat':
        '''SpecificHeat: 'Measurement' is the original name of this property.'''

        if _1450.SpecificHeat.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SpecificHeat. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_specific_heat.setter
    def measurement_of_type_specific_heat(self, value: '_1450.SpecificHeat'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1451.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'Measurement' is the original name of this property.'''

        if _1451.SquareRootOfUnitForcePerUnitArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_square_root_of_unit_force_per_unit_area.setter
    def measurement_of_type_square_root_of_unit_force_per_unit_area(self, value: '_1451.SquareRootOfUnitForcePerUnitArea'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_stiffness_per_unit_face_width(self) -> '_1452.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'Measurement' is the original name of this property.'''

        if _1452.StiffnessPerUnitFaceWidth.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_stiffness_per_unit_face_width.setter
    def measurement_of_type_stiffness_per_unit_face_width(self, value: '_1452.StiffnessPerUnitFaceWidth'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_stress(self) -> '_1453.Stress':
        '''Stress: 'Measurement' is the original name of this property.'''

        if _1453.Stress.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Stress. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_stress.setter
    def measurement_of_type_stress(self, value: '_1453.Stress'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_temperature(self) -> '_1454.Temperature':
        '''Temperature: 'Measurement' is the original name of this property.'''

        if _1454.Temperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Temperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_temperature.setter
    def measurement_of_type_temperature(self, value: '_1454.Temperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_temperature_difference(self) -> '_1455.TemperatureDifference':
        '''TemperatureDifference: 'Measurement' is the original name of this property.'''

        if _1455.TemperatureDifference.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TemperatureDifference. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_temperature_difference.setter
    def measurement_of_type_temperature_difference(self, value: '_1455.TemperatureDifference'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_temperature_per_unit_time(self) -> '_1456.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'Measurement' is the original name of this property.'''

        if _1456.TemperaturePerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TemperaturePerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_temperature_per_unit_time.setter
    def measurement_of_type_temperature_per_unit_time(self, value: '_1456.TemperaturePerUnitTime'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_text(self) -> '_1457.Text':
        '''Text: 'Measurement' is the original name of this property.'''

        if _1457.Text.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Text. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_text.setter
    def measurement_of_type_text(self, value: '_1457.Text'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_thermal_contact_coefficient(self) -> '_1458.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'Measurement' is the original name of this property.'''

        if _1458.ThermalContactCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermalContactCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_thermal_contact_coefficient.setter
    def measurement_of_type_thermal_contact_coefficient(self, value: '_1458.ThermalContactCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_thermal_expansion_coefficient(self) -> '_1459.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'Measurement' is the original name of this property.'''

        if _1459.ThermalExpansionCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermalExpansionCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_thermal_expansion_coefficient.setter
    def measurement_of_type_thermal_expansion_coefficient(self, value: '_1459.ThermalExpansionCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_thermo_elastic_factor(self) -> '_1460.ThermoElasticFactor':
        '''ThermoElasticFactor: 'Measurement' is the original name of this property.'''

        if _1460.ThermoElasticFactor.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermoElasticFactor. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_thermo_elastic_factor.setter
    def measurement_of_type_thermo_elastic_factor(self, value: '_1460.ThermoElasticFactor'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_time(self) -> '_1461.Time':
        '''Time: 'Measurement' is the original name of this property.'''

        if _1461.Time.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Time. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_time.setter
    def measurement_of_type_time(self, value: '_1461.Time'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_time_short(self) -> '_1462.TimeShort':
        '''TimeShort: 'Measurement' is the original name of this property.'''

        if _1462.TimeShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TimeShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_time_short.setter
    def measurement_of_type_time_short(self, value: '_1462.TimeShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_time_very_short(self) -> '_1463.TimeVeryShort':
        '''TimeVeryShort: 'Measurement' is the original name of this property.'''

        if _1463.TimeVeryShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TimeVeryShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_time_very_short.setter
    def measurement_of_type_time_very_short(self, value: '_1463.TimeVeryShort'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque(self) -> '_1464.Torque':
        '''Torque: 'Measurement' is the original name of this property.'''

        if _1464.Torque.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Torque. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_torque.setter
    def measurement_of_type_torque(self, value: '_1464.Torque'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque_converter_inverse_k(self) -> '_1465.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'Measurement' is the original name of this property.'''

        if _1465.TorqueConverterInverseK.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorqueConverterInverseK. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_torque_converter_inverse_k.setter
    def measurement_of_type_torque_converter_inverse_k(self, value: '_1465.TorqueConverterInverseK'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque_converter_k(self) -> '_1466.TorqueConverterK':
        '''TorqueConverterK: 'Measurement' is the original name of this property.'''

        if _1466.TorqueConverterK.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorqueConverterK. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_torque_converter_k.setter
    def measurement_of_type_torque_converter_k(self, value: '_1466.TorqueConverterK'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_torque_per_unit_temperature(self) -> '_1467.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'Measurement' is the original name of this property.'''

        if _1467.TorquePerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorquePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_torque_per_unit_temperature.setter
    def measurement_of_type_torque_per_unit_temperature(self, value: '_1467.TorquePerUnitTemperature'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_velocity(self) -> '_1468.Velocity':
        '''Velocity: 'Measurement' is the original name of this property.'''

        if _1468.Velocity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Velocity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_velocity.setter
    def measurement_of_type_velocity(self, value: '_1468.Velocity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_velocity_small(self) -> '_1469.VelocitySmall':
        '''VelocitySmall: 'Measurement' is the original name of this property.'''

        if _1469.VelocitySmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to VelocitySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_velocity_small.setter
    def measurement_of_type_velocity_small(self, value: '_1469.VelocitySmall'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_viscosity(self) -> '_1470.Viscosity':
        '''Viscosity: 'Measurement' is the original name of this property.'''

        if _1470.Viscosity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Viscosity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_viscosity.setter
    def measurement_of_type_viscosity(self, value: '_1470.Viscosity'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_voltage(self) -> '_1471.Voltage':
        '''Voltage: 'Measurement' is the original name of this property.'''

        if _1471.Voltage.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Voltage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_voltage.setter
    def measurement_of_type_voltage(self, value: '_1471.Voltage'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_volume(self) -> '_1472.Volume':
        '''Volume: 'Measurement' is the original name of this property.'''

        if _1472.Volume.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Volume. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_volume.setter
    def measurement_of_type_volume(self, value: '_1472.Volume'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_wear_coefficient(self) -> '_1473.WearCoefficient':
        '''WearCoefficient: 'Measurement' is the original name of this property.'''

        if _1473.WearCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to WearCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_wear_coefficient.setter
    def measurement_of_type_wear_coefficient(self, value: '_1473.WearCoefficient'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def measurement_of_type_yank(self) -> '_1474.Yank':
        '''Yank: 'Measurement' is the original name of this property.'''

        if _1474.Yank.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Yank. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Measurement.__class__)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @measurement_of_type_yank.setter
    def measurement_of_type_yank(self, value: '_1474.Yank'):
        value = value.wrapped if value else None
        self.wrapped.Measurement = value

    @property
    def results(self) -> 'List[float]':
        '''List[float]: 'Results' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Results, float)
        return value
