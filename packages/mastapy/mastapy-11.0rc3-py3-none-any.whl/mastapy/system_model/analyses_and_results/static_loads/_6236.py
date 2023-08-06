﻿'''_6236.py

PowerLoadLoadCase
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model import _1846, _1847, _1848
from mastapy.system_model.analyses_and_results.mbd_analyses import _5164
from mastapy.system_model.analyses_and_results.static_loads import _6274, _6173, _6278
from mastapy.system_model.imported_fes import _1981
from mastapy.system_model.part_model import _2072
from mastapy.math_utility.control import _1143
from mastapy.nodal_analysis.varying_input_components import _1419
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PowerLoadLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadLoadCase',)


class PowerLoadLoadCase(_6278.VirtualComponentLoadCase):
    '''PowerLoadLoadCase

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def torque_time_profile_repeats(self) -> 'bool':
        '''bool: 'TorqueTimeProfileRepeats' is the original name of this property.'''

        return self.wrapped.TorqueTimeProfileRepeats

    @torque_time_profile_repeats.setter
    def torque_time_profile_repeats(self, value: 'bool'):
        self.wrapped.TorqueTimeProfileRepeats = bool(value) if value else False

    @property
    def engine_throttle_position(self) -> 'float':
        '''float: 'EngineThrottlePosition' is the original name of this property.'''

        return self.wrapped.EngineThrottlePosition

    @engine_throttle_position.setter
    def engine_throttle_position(self, value: 'float'):
        self.wrapped.EngineThrottlePosition = float(value) if value else 0.0

    @property
    def use_engine_idle_speed_control(self) -> 'bool':
        '''bool: 'UseEngineIdleSpeedControl' is the original name of this property.'''

        return self.wrapped.UseEngineIdleSpeedControl

    @use_engine_idle_speed_control.setter
    def use_engine_idle_speed_control(self, value: 'bool'):
        self.wrapped.UseEngineIdleSpeedControl = bool(value) if value else False

    @property
    def vehicle_speed_to_start_idle_control(self) -> 'float':
        '''float: 'VehicleSpeedToStartIdleControl' is the original name of this property.'''

        return self.wrapped.VehicleSpeedToStartIdleControl

    @vehicle_speed_to_start_idle_control.setter
    def vehicle_speed_to_start_idle_control(self, value: 'float'):
        self.wrapped.VehicleSpeedToStartIdleControl = float(value) if value else 0.0

    @property
    def vehicle_speed_to_stop_idle_control(self) -> 'float':
        '''float: 'VehicleSpeedToStopIdleControl' is the original name of this property.'''

        return self.wrapped.VehicleSpeedToStopIdleControl

    @vehicle_speed_to_stop_idle_control.setter
    def vehicle_speed_to_stop_idle_control(self, value: 'float'):
        self.wrapped.VehicleSpeedToStopIdleControl = float(value) if value else 0.0

    @property
    def target_engine_idle_speed(self) -> 'float':
        '''float: 'TargetEngineIdleSpeed' is the original name of this property.'''

        return self.wrapped.TargetEngineIdleSpeed

    @target_engine_idle_speed.setter
    def target_engine_idle_speed(self, value: 'float'):
        self.wrapped.TargetEngineIdleSpeed = float(value) if value else 0.0

    @property
    def first_order_lag_time_constant(self) -> 'float':
        '''float: 'FirstOrderLagTimeConstant' is the original name of this property.'''

        return self.wrapped.FirstOrderLagTimeConstant

    @first_order_lag_time_constant.setter
    def first_order_lag_time_constant(self, value: 'float'):
        self.wrapped.FirstOrderLagTimeConstant = float(value) if value else 0.0

    @property
    def first_order_lag_cutoff_frequency(self) -> 'float':
        '''float: 'FirstOrderLagCutoffFrequency' is the original name of this property.'''

        return self.wrapped.FirstOrderLagCutoffFrequency

    @first_order_lag_cutoff_frequency.setter
    def first_order_lag_cutoff_frequency(self, value: 'float'):
        self.wrapped.FirstOrderLagCutoffFrequency = float(value) if value else 0.0

    @property
    def constant_resistance_coefficient(self) -> 'float':
        '''float: 'ConstantResistanceCoefficient' is the original name of this property.'''

        return self.wrapped.ConstantResistanceCoefficient

    @constant_resistance_coefficient.setter
    def constant_resistance_coefficient(self, value: 'float'):
        self.wrapped.ConstantResistanceCoefficient = float(value) if value else 0.0

    @property
    def linear_resistance_coefficient(self) -> 'float':
        '''float: 'LinearResistanceCoefficient' is the original name of this property.'''

        return self.wrapped.LinearResistanceCoefficient

    @linear_resistance_coefficient.setter
    def linear_resistance_coefficient(self, value: 'float'):
        self.wrapped.LinearResistanceCoefficient = float(value) if value else 0.0

    @property
    def quadratic_resistance_coefficient(self) -> 'float':
        '''float: 'QuadraticResistanceCoefficient' is the original name of this property.'''

        return self.wrapped.QuadraticResistanceCoefficient

    @quadratic_resistance_coefficient.setter
    def quadratic_resistance_coefficient(self, value: 'float'):
        self.wrapped.QuadraticResistanceCoefficient = float(value) if value else 0.0

    @property
    def power(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Power' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Power) if self.wrapped.Power else None

    @power.setter
    def power(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Power = value

    @property
    def torque(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Torque' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Torque) if self.wrapped.Torque else None

    @torque.setter
    def torque(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Torque = value

    @property
    def constant_torque(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ConstantTorque' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ConstantTorque) if self.wrapped.ConstantTorque else None

    @constant_torque.setter
    def constant_torque(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ConstantTorque = value

    @property
    def speed(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Speed' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Speed) if self.wrapped.Speed else None

    @speed.setter
    def speed(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Speed = value

    @property
    def use_time_dependent_quadratic_resistance_coefficient(self) -> 'bool':
        '''bool: 'UseTimeDependentQuadraticResistanceCoefficient' is the original name of this property.'''

        return self.wrapped.UseTimeDependentQuadraticResistanceCoefficient

    @use_time_dependent_quadratic_resistance_coefficient.setter
    def use_time_dependent_quadratic_resistance_coefficient(self, value: 'bool'):
        self.wrapped.UseTimeDependentQuadraticResistanceCoefficient = bool(value) if value else False

    @property
    def use_time_dependent_linear_resistance_coefficient(self) -> 'bool':
        '''bool: 'UseTimeDependentLinearResistanceCoefficient' is the original name of this property.'''

        return self.wrapped.UseTimeDependentLinearResistanceCoefficient

    @use_time_dependent_linear_resistance_coefficient.setter
    def use_time_dependent_linear_resistance_coefficient(self, value: 'bool'):
        self.wrapped.UseTimeDependentLinearResistanceCoefficient = bool(value) if value else False

    @property
    def use_time_dependent_constant_resistance_coefficient(self) -> 'bool':
        '''bool: 'UseTimeDependentConstantResistanceCoefficient' is the original name of this property.'''

        return self.wrapped.UseTimeDependentConstantResistanceCoefficient

    @use_time_dependent_constant_resistance_coefficient.setter
    def use_time_dependent_constant_resistance_coefficient(self, value: 'bool'):
        self.wrapped.UseTimeDependentConstantResistanceCoefficient = bool(value) if value else False

    @property
    def drag_torque_specification_method(self) -> '_1846.PowerLoadDragTorqueSpecificationMethod':
        '''PowerLoadDragTorqueSpecificationMethod: 'DragTorqueSpecificationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.DragTorqueSpecificationMethod)
        return constructor.new(_1846.PowerLoadDragTorqueSpecificationMethod)(value) if value else None

    @drag_torque_specification_method.setter
    def drag_torque_specification_method(self, value: '_1846.PowerLoadDragTorqueSpecificationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DragTorqueSpecificationMethod = value

    @property
    def use_time_dependent_throttle(self) -> 'bool':
        '''bool: 'UseTimeDependentThrottle' is the original name of this property.'''

        return self.wrapped.UseTimeDependentThrottle

    @use_time_dependent_throttle.setter
    def use_time_dependent_throttle(self, value: 'bool'):
        self.wrapped.UseTimeDependentThrottle = bool(value) if value else False

    @property
    def wheel_slip_model(self) -> '_5164.WheelSlipType':
        '''WheelSlipType: 'WheelSlipModel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.WheelSlipModel)
        return constructor.new(_5164.WheelSlipType)(value) if value else None

    @wheel_slip_model.setter
    def wheel_slip_model(self, value: '_5164.WheelSlipType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WheelSlipModel = value

    @property
    def wheel_static_to_dynamic_friction_ratio(self) -> 'float':
        '''float: 'WheelStaticToDynamicFrictionRatio' is the original name of this property.'''

        return self.wrapped.WheelStaticToDynamicFrictionRatio

    @wheel_static_to_dynamic_friction_ratio.setter
    def wheel_static_to_dynamic_friction_ratio(self, value: 'float'):
        self.wrapped.WheelStaticToDynamicFrictionRatio = float(value) if value else 0.0

    @property
    def wheel_to_vehicle_stiffness(self) -> 'float':
        '''float: 'WheelToVehicleStiffness' is the original name of this property.'''

        return self.wrapped.WheelToVehicleStiffness

    @wheel_to_vehicle_stiffness.setter
    def wheel_to_vehicle_stiffness(self, value: 'float'):
        self.wrapped.WheelToVehicleStiffness = float(value) if value else 0.0

    @property
    def is_wheel_using_static_friction_initially(self) -> 'bool':
        '''bool: 'IsWheelUsingStaticFrictionInitially' is the original name of this property.'''

        return self.wrapped.IsWheelUsingStaticFrictionInitially

    @is_wheel_using_static_friction_initially.setter
    def is_wheel_using_static_friction_initially(self, value: 'bool'):
        self.wrapped.IsWheelUsingStaticFrictionInitially = bool(value) if value else False

    @property
    def proportion_of_vehicle_weight_carried(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ProportionOfVehicleWeightCarried' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ProportionOfVehicleWeightCarried) if self.wrapped.ProportionOfVehicleWeightCarried else None

    @proportion_of_vehicle_weight_carried.setter
    def proportion_of_vehicle_weight_carried(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ProportionOfVehicleWeightCarried = value

    @property
    def specify_initial_displacement(self) -> 'bool':
        '''bool: 'SpecifyInitialDisplacement' is the original name of this property.'''

        return self.wrapped.SpecifyInitialDisplacement

    @specify_initial_displacement.setter
    def specify_initial_displacement(self, value: 'bool'):
        self.wrapped.SpecifyInitialDisplacement = bool(value) if value else False

    @property
    def specify_initial_velocity(self) -> 'bool':
        '''bool: 'SpecifyInitialVelocity' is the original name of this property.'''

        return self.wrapped.SpecifyInitialVelocity

    @specify_initial_velocity.setter
    def specify_initial_velocity(self, value: 'bool'):
        self.wrapped.SpecifyInitialVelocity = bool(value) if value else False

    @property
    def specify_initial_acceleration(self) -> 'bool':
        '''bool: 'SpecifyInitialAcceleration' is the original name of this property.'''

        return self.wrapped.SpecifyInitialAcceleration

    @specify_initial_acceleration.setter
    def specify_initial_acceleration(self, value: 'bool'):
        self.wrapped.SpecifyInitialAcceleration = bool(value) if value else False

    @property
    def initial_angular_displacement(self) -> 'float':
        '''float: 'InitialAngularDisplacement' is the original name of this property.'''

        return self.wrapped.InitialAngularDisplacement

    @initial_angular_displacement.setter
    def initial_angular_displacement(self, value: 'float'):
        self.wrapped.InitialAngularDisplacement = float(value) if value else 0.0

    @property
    def initial_angular_velocity(self) -> 'float':
        '''float: 'InitialAngularVelocity' is the original name of this property.'''

        return self.wrapped.InitialAngularVelocity

    @initial_angular_velocity.setter
    def initial_angular_velocity(self, value: 'float'):
        self.wrapped.InitialAngularVelocity = float(value) if value else 0.0

    @property
    def initial_angular_acceleration(self) -> 'float':
        '''float: 'InitialAngularAcceleration' is the original name of this property.'''

        return self.wrapped.InitialAngularAcceleration

    @initial_angular_acceleration.setter
    def initial_angular_acceleration(self, value: 'float'):
        self.wrapped.InitialAngularAcceleration = float(value) if value else 0.0

    @property
    def unbalanced_magnetic_pull_stiffness(self) -> 'float':
        '''float: 'UnbalancedMagneticPullStiffness' is the original name of this property.'''

        return self.wrapped.UnbalancedMagneticPullStiffness

    @unbalanced_magnetic_pull_stiffness.setter
    def unbalanced_magnetic_pull_stiffness(self, value: 'float'):
        self.wrapped.UnbalancedMagneticPullStiffness = float(value) if value else 0.0

    @property
    def dynamic_torsional_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DynamicTorsionalStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DynamicTorsionalStiffness) if self.wrapped.DynamicTorsionalStiffness else None

    @dynamic_torsional_stiffness.setter
    def dynamic_torsional_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.DynamicTorsionalStiffness = value

    @property
    def input_torque_specification_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod: 'InputTorqueSpecificationMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.InputTorqueSpecificationMethod, value) if self.wrapped.InputTorqueSpecificationMethod else None

    @input_torque_specification_method.setter
    def input_torque_specification_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.InputTorqueSpecificationMethod = value

    @property
    def power_load_for_pid_control(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'PowerLoadForPIDControl' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.PowerLoadForPIDControl) if self.wrapped.PowerLoadForPIDControl else None

    @power_load_for_pid_control.setter
    def power_load_for_pid_control(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.PowerLoadForPIDControl = value

    @property
    def target_speed_input_type(self) -> '_1848.PowerLoadPIDControlSpeedInputType':
        '''PowerLoadPIDControlSpeedInputType: 'TargetSpeedInputType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TargetSpeedInputType)
        return constructor.new(_1848.PowerLoadPIDControlSpeedInputType)(value) if value else None

    @target_speed_input_type.setter
    def target_speed_input_type(self, value: '_1848.PowerLoadPIDControlSpeedInputType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TargetSpeedInputType = value

    @property
    def target_speed(self) -> 'float':
        '''float: 'TargetSpeed' is the original name of this property.'''

        return self.wrapped.TargetSpeed

    @target_speed.setter
    def target_speed(self, value: 'float'):
        self.wrapped.TargetSpeed = float(value) if value else 0.0

    @property
    def maximum_throttle_in_drive_cycle(self) -> 'float':
        '''float: 'MaximumThrottleInDriveCycle' is the original name of this property.'''

        return self.wrapped.MaximumThrottleInDriveCycle

    @maximum_throttle_in_drive_cycle.setter
    def maximum_throttle_in_drive_cycle(self, value: 'float'):
        self.wrapped.MaximumThrottleInDriveCycle = float(value) if value else 0.0

    @property
    def torque_specification_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection':
        '''enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection: 'TorqueSpecificationMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.TorqueSpecificationMethod, value) if self.wrapped.TorqueSpecificationMethod else None

    @torque_specification_method.setter
    def torque_specification_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.TorqueSpecificationMethod = value

    @property
    def specified_angle_for_input_torque(self) -> 'float':
        '''float: 'SpecifiedAngleForInputTorque' is the original name of this property.'''

        return self.wrapped.SpecifiedAngleForInputTorque

    @specified_angle_for_input_torque.setter
    def specified_angle_for_input_torque(self, value: 'float'):
        self.wrapped.SpecifiedAngleForInputTorque = float(value) if value else 0.0

    @property
    def specified_time_for_input_torque(self) -> 'float':
        '''float: 'SpecifiedTimeForInputTorque' is the original name of this property.'''

        return self.wrapped.SpecifiedTimeForInputTorque

    @specified_time_for_input_torque.setter
    def specified_time_for_input_torque(self, value: 'float'):
        self.wrapped.SpecifiedTimeForInputTorque = float(value) if value else 0.0

    @property
    def electric_machine_data_set_selector(self) -> 'list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet':
        '''list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet: 'ElectricMachineDataSetSelector' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet)(self.wrapped.ElectricMachineDataSetSelector) if self.wrapped.ElectricMachineDataSetSelector else None

    @electric_machine_data_set_selector.setter
    def electric_machine_data_set_selector(self, value: 'list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ElectricMachineDataSetSelector = value

    @property
    def total_mean_rotor_x_force_over_all_nodes(self) -> 'float':
        '''float: 'TotalMeanRotorXForceOverAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMeanRotorXForceOverAllNodes

    @property
    def total_mean_rotor_y_force_over_all_nodes(self) -> 'float':
        '''float: 'TotalMeanRotorYForceOverAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMeanRotorYForceOverAllNodes

    @property
    def component_design(self) -> '_2072.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2072.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def engine_idle_speed_control_pid_settings(self) -> '_1143.PIDControlSettings':
        '''PIDControlSettings: 'EngineIdleSpeedControlPIDSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1143.PIDControlSettings)(self.wrapped.EngineIdleSpeedControlPIDSettings) if self.wrapped.EngineIdleSpeedControlPIDSettings else None

    @property
    def coefficient_of_friction_with_ground(self) -> '_1419.NonDimensionalInputComponent':
        '''NonDimensionalInputComponent: 'CoefficientOfFrictionWithGround' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1419.NonDimensionalInputComponent)(self.wrapped.CoefficientOfFrictionWithGround) if self.wrapped.CoefficientOfFrictionWithGround else None

    @property
    def pid_control_settings(self) -> '_1143.PIDControlSettings':
        '''PIDControlSettings: 'PIDControlSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1143.PIDControlSettings)(self.wrapped.PIDControlSettings) if self.wrapped.PIDControlSettings else None

    def get_harmonic_load_data_for_import(self) -> '_6173.ElectricMachineHarmonicLoadData':
        ''' 'GetHarmonicLoadDataForImport' is the original name of this method.

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ElectricMachineHarmonicLoadData
        '''

        method_result = self.wrapped.GetHarmonicLoadDataForImport()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
