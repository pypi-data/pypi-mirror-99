﻿'''_493.py

GearCutterSimulation
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import (
    _490, _498, _485, _492,
    _494, _497, _499, _500,
    _501, _502, _488, _489
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_CUTTER_SIMULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'GearCutterSimulation')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCutterSimulation',)


class GearCutterSimulation(_0.APIBase):
    '''GearCutterSimulation

    This is a mastapy class.
    '''

    TYPE = _GEAR_CUTTER_SIMULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCutterSimulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def highest_finished_form_diameter(self) -> 'float':
        '''float: 'HighestFinishedFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HighestFinishedFormDiameter

    @property
    def lowest_finished_tip_form_diameter(self) -> 'float':
        '''float: 'LowestFinishedTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LowestFinishedTipFormDiameter

    @property
    def least_sap_to_form_radius_clearance(self) -> 'float':
        '''float: 'LeastSAPToFormRadiusClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LeastSAPToFormRadiusClearance

    @property
    def cutter_simulation(self) -> 'GearCutterSimulation':
        '''GearCutterSimulation: 'CutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if GearCutterSimulation.TYPE not in self.wrapped.CutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast cutter_simulation to GearCutterSimulation. Expected: {}.'.format(self.wrapped.CutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CutterSimulation.__class__)(self.wrapped.CutterSimulation) if self.wrapped.CutterSimulation else None

    @property
    def cutter_simulation_of_type_finish_cutter_simulation(self) -> '_490.FinishCutterSimulation':
        '''FinishCutterSimulation: 'CutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _490.FinishCutterSimulation.TYPE not in self.wrapped.CutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast cutter_simulation to FinishCutterSimulation. Expected: {}.'.format(self.wrapped.CutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CutterSimulation.__class__)(self.wrapped.CutterSimulation) if self.wrapped.CutterSimulation else None

    @property
    def cutter_simulation_of_type_rough_cutter_simulation(self) -> '_498.RoughCutterSimulation':
        '''RoughCutterSimulation: 'CutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _498.RoughCutterSimulation.TYPE not in self.wrapped.CutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast cutter_simulation to RoughCutterSimulation. Expected: {}.'.format(self.wrapped.CutterSimulation.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CutterSimulation.__class__)(self.wrapped.CutterSimulation) if self.wrapped.CutterSimulation else None

    @property
    def minimum_thickness(self) -> '_485.CutterSimulationCalc':
        '''CutterSimulationCalc: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _485.CutterSimulationCalc.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to CutterSimulationCalc. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def minimum_thickness_of_type_form_wheel_grinding_simulation_calculator(self) -> '_492.FormWheelGrindingSimulationCalculator':
        '''FormWheelGrindingSimulationCalculator: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _492.FormWheelGrindingSimulationCalculator.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to FormWheelGrindingSimulationCalculator. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def minimum_thickness_of_type_hob_simulation_calculator(self) -> '_494.HobSimulationCalculator':
        '''HobSimulationCalculator: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _494.HobSimulationCalculator.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to HobSimulationCalculator. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def minimum_thickness_of_type_rack_simulation_calculator(self) -> '_497.RackSimulationCalculator':
        '''RackSimulationCalculator: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _497.RackSimulationCalculator.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to RackSimulationCalculator. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def minimum_thickness_of_type_shaper_simulation_calculator(self) -> '_499.ShaperSimulationCalculator':
        '''ShaperSimulationCalculator: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ShaperSimulationCalculator.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to ShaperSimulationCalculator. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def minimum_thickness_of_type_shaving_simulation_calculator(self) -> '_500.ShavingSimulationCalculator':
        '''ShavingSimulationCalculator: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _500.ShavingSimulationCalculator.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to ShavingSimulationCalculator. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def minimum_thickness_of_type_virtual_simulation_calculator(self) -> '_501.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.VirtualSimulationCalculator.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to VirtualSimulationCalculator. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def minimum_thickness_of_type_worm_grinder_simulation_calculator(self) -> '_502.WormGrinderSimulationCalculator':
        '''WormGrinderSimulationCalculator: 'MinimumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.WormGrinderSimulationCalculator.TYPE not in self.wrapped.MinimumThickness.__class__.__mro__:
            raise CastException('Failed to cast minimum_thickness to WormGrinderSimulationCalculator. Expected: {}.'.format(self.wrapped.MinimumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MinimumThickness.__class__)(self.wrapped.MinimumThickness) if self.wrapped.MinimumThickness else None

    @property
    def average_thickness(self) -> '_485.CutterSimulationCalc':
        '''CutterSimulationCalc: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _485.CutterSimulationCalc.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to CutterSimulationCalc. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def average_thickness_of_type_form_wheel_grinding_simulation_calculator(self) -> '_492.FormWheelGrindingSimulationCalculator':
        '''FormWheelGrindingSimulationCalculator: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _492.FormWheelGrindingSimulationCalculator.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to FormWheelGrindingSimulationCalculator. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def average_thickness_of_type_hob_simulation_calculator(self) -> '_494.HobSimulationCalculator':
        '''HobSimulationCalculator: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _494.HobSimulationCalculator.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to HobSimulationCalculator. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def average_thickness_of_type_rack_simulation_calculator(self) -> '_497.RackSimulationCalculator':
        '''RackSimulationCalculator: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _497.RackSimulationCalculator.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to RackSimulationCalculator. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def average_thickness_of_type_shaper_simulation_calculator(self) -> '_499.ShaperSimulationCalculator':
        '''ShaperSimulationCalculator: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ShaperSimulationCalculator.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to ShaperSimulationCalculator. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def average_thickness_of_type_shaving_simulation_calculator(self) -> '_500.ShavingSimulationCalculator':
        '''ShavingSimulationCalculator: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _500.ShavingSimulationCalculator.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to ShavingSimulationCalculator. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def average_thickness_of_type_virtual_simulation_calculator(self) -> '_501.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.VirtualSimulationCalculator.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to VirtualSimulationCalculator. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def average_thickness_of_type_worm_grinder_simulation_calculator(self) -> '_502.WormGrinderSimulationCalculator':
        '''WormGrinderSimulationCalculator: 'AverageThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.WormGrinderSimulationCalculator.TYPE not in self.wrapped.AverageThickness.__class__.__mro__:
            raise CastException('Failed to cast average_thickness to WormGrinderSimulationCalculator. Expected: {}.'.format(self.wrapped.AverageThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AverageThickness.__class__)(self.wrapped.AverageThickness) if self.wrapped.AverageThickness else None

    @property
    def maximum_thickness(self) -> '_485.CutterSimulationCalc':
        '''CutterSimulationCalc: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _485.CutterSimulationCalc.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to CutterSimulationCalc. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def maximum_thickness_of_type_form_wheel_grinding_simulation_calculator(self) -> '_492.FormWheelGrindingSimulationCalculator':
        '''FormWheelGrindingSimulationCalculator: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _492.FormWheelGrindingSimulationCalculator.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to FormWheelGrindingSimulationCalculator. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def maximum_thickness_of_type_hob_simulation_calculator(self) -> '_494.HobSimulationCalculator':
        '''HobSimulationCalculator: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _494.HobSimulationCalculator.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to HobSimulationCalculator. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def maximum_thickness_of_type_rack_simulation_calculator(self) -> '_497.RackSimulationCalculator':
        '''RackSimulationCalculator: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _497.RackSimulationCalculator.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to RackSimulationCalculator. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def maximum_thickness_of_type_shaper_simulation_calculator(self) -> '_499.ShaperSimulationCalculator':
        '''ShaperSimulationCalculator: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ShaperSimulationCalculator.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to ShaperSimulationCalculator. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def maximum_thickness_of_type_shaving_simulation_calculator(self) -> '_500.ShavingSimulationCalculator':
        '''ShavingSimulationCalculator: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _500.ShavingSimulationCalculator.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to ShavingSimulationCalculator. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def maximum_thickness_of_type_virtual_simulation_calculator(self) -> '_501.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.VirtualSimulationCalculator.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to VirtualSimulationCalculator. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def maximum_thickness_of_type_worm_grinder_simulation_calculator(self) -> '_502.WormGrinderSimulationCalculator':
        '''WormGrinderSimulationCalculator: 'MaximumThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.WormGrinderSimulationCalculator.TYPE not in self.wrapped.MaximumThickness.__class__.__mro__:
            raise CastException('Failed to cast maximum_thickness to WormGrinderSimulationCalculator. Expected: {}.'.format(self.wrapped.MaximumThickness.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MaximumThickness.__class__)(self.wrapped.MaximumThickness) if self.wrapped.MaximumThickness else None

    @property
    def smallest_active_profile(self) -> '_485.CutterSimulationCalc':
        '''CutterSimulationCalc: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _485.CutterSimulationCalc.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to CutterSimulationCalc. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def smallest_active_profile_of_type_form_wheel_grinding_simulation_calculator(self) -> '_492.FormWheelGrindingSimulationCalculator':
        '''FormWheelGrindingSimulationCalculator: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _492.FormWheelGrindingSimulationCalculator.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to FormWheelGrindingSimulationCalculator. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def smallest_active_profile_of_type_hob_simulation_calculator(self) -> '_494.HobSimulationCalculator':
        '''HobSimulationCalculator: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _494.HobSimulationCalculator.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to HobSimulationCalculator. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def smallest_active_profile_of_type_rack_simulation_calculator(self) -> '_497.RackSimulationCalculator':
        '''RackSimulationCalculator: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _497.RackSimulationCalculator.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to RackSimulationCalculator. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def smallest_active_profile_of_type_shaper_simulation_calculator(self) -> '_499.ShaperSimulationCalculator':
        '''ShaperSimulationCalculator: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ShaperSimulationCalculator.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to ShaperSimulationCalculator. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def smallest_active_profile_of_type_shaving_simulation_calculator(self) -> '_500.ShavingSimulationCalculator':
        '''ShavingSimulationCalculator: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _500.ShavingSimulationCalculator.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to ShavingSimulationCalculator. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def smallest_active_profile_of_type_virtual_simulation_calculator(self) -> '_501.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.VirtualSimulationCalculator.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to VirtualSimulationCalculator. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def smallest_active_profile_of_type_worm_grinder_simulation_calculator(self) -> '_502.WormGrinderSimulationCalculator':
        '''WormGrinderSimulationCalculator: 'SmallestActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.WormGrinderSimulationCalculator.TYPE not in self.wrapped.SmallestActiveProfile.__class__.__mro__:
            raise CastException('Failed to cast smallest_active_profile to WormGrinderSimulationCalculator. Expected: {}.'.format(self.wrapped.SmallestActiveProfile.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SmallestActiveProfile.__class__)(self.wrapped.SmallestActiveProfile) if self.wrapped.SmallestActiveProfile else None

    @property
    def minimum_thickness_virtual(self) -> '_501.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'MinimumThicknessVirtual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_501.VirtualSimulationCalculator)(self.wrapped.MinimumThicknessVirtual) if self.wrapped.MinimumThicknessVirtual else None

    @property
    def average_thickness_virtual(self) -> '_501.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'AverageThicknessVirtual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_501.VirtualSimulationCalculator)(self.wrapped.AverageThicknessVirtual) if self.wrapped.AverageThicknessVirtual else None

    @property
    def maximum_thickness_virtual(self) -> '_501.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'MaximumThicknessVirtual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_501.VirtualSimulationCalculator)(self.wrapped.MaximumThicknessVirtual) if self.wrapped.MaximumThicknessVirtual else None

    @property
    def thickness_calculators(self) -> 'List[_485.CutterSimulationCalc]':
        '''List[CutterSimulationCalc]: 'ThicknessCalculators' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ThicknessCalculators, constructor.new(_485.CutterSimulationCalc))
        return value

    @property
    def virtual_thickness_calculators(self) -> 'List[_501.VirtualSimulationCalculator]':
        '''List[VirtualSimulationCalculator]: 'VirtualThicknessCalculators' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.VirtualThicknessCalculators, constructor.new(_501.VirtualSimulationCalculator))
        return value

    @property
    def gear_mesh_cutter_simulations(self) -> 'List[_488.CylindricalManufacturedRealGearInMesh]':
        '''List[CylindricalManufacturedRealGearInMesh]: 'GearMeshCutterSimulations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshCutterSimulations, constructor.new(_488.CylindricalManufacturedRealGearInMesh))
        return value

    @property
    def gear_mesh_cutter_simulations_virtual(self) -> 'List[_489.CylindricalManufacturedVirtualGearInMesh]':
        '''List[CylindricalManufacturedVirtualGearInMesh]: 'GearMeshCutterSimulationsVirtual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshCutterSimulationsVirtual, constructor.new(_489.CylindricalManufacturedVirtualGearInMesh))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
