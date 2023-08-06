﻿'''_548.py

ShavingDynamicsCalculation
'''


from typing import (
    Callable, List, Generic, TypeVar
)

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _544, _543, _547
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _486
from mastapy.gears.manufacturing.cylindrical.cutters import _515, _510
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _783
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsCalculation',)


T = TypeVar('T', bound='_547.ShavingDynamics')


class ShavingDynamicsCalculation(_0.APIBase, Generic[T]):
    '''ShavingDynamicsCalculation

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _SHAVING_DYNAMICS_CALCULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamicsCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cutter_simulation_calculation_required(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CutterSimulationCalculationRequired' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterSimulationCalculationRequired

    @property
    def life_cutter_tip_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LifeCutterTipDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LifeCutterTipDiameter) if self.wrapped.LifeCutterTipDiameter else None

    @life_cutter_tip_diameter.setter
    def life_cutter_tip_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.LifeCutterTipDiameter = value

    @property
    def new_cutter_tip_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NewCutterTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NewCutterTipDiameter) if self.wrapped.NewCutterTipDiameter else None

    @property
    def selected_redressing(self) -> 'list_with_selected_item.ListWithSelectedItem_T':
        '''list_with_selected_item.ListWithSelectedItem_T: 'SelectedRedressing' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_T)(self.wrapped.SelectedRedressing) if self.wrapped.SelectedRedressing else None

    @selected_redressing.setter
    def selected_redressing(self, value: 'list_with_selected_item.ListWithSelectedItem_T.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_T.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedRedressing = value

    @property
    def normal_tooth_thickness_reduction_between_redressings(self) -> 'float':
        '''float: 'NormalToothThicknessReductionBetweenRedressings' is the original name of this property.'''

        return self.wrapped.NormalToothThicknessReductionBetweenRedressings

    @normal_tooth_thickness_reduction_between_redressings.setter
    def normal_tooth_thickness_reduction_between_redressings(self, value: 'float'):
        self.wrapped.NormalToothThicknessReductionBetweenRedressings = float(value) if value else 0.0

    @property
    def life_cutter_normal_thickness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LifeCutterNormalThickness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LifeCutterNormalThickness) if self.wrapped.LifeCutterNormalThickness else None

    @life_cutter_normal_thickness.setter
    def life_cutter_normal_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.LifeCutterNormalThickness = value

    @property
    def adjusted_tip_diameter(self) -> 'List[float]':
        '''List[float]: 'AdjustedTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.AdjustedTipDiameter)
        return value

    @property
    def accuracy_level_iso6(self) -> '_544.RollAngleRangeRelativeToAccuracy':
        '''RollAngleRangeRelativeToAccuracy: 'AccuracyLevelISO6' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_544.RollAngleRangeRelativeToAccuracy)(self.wrapped.AccuracyLevelISO6) if self.wrapped.AccuracyLevelISO6 else None

    @property
    def accuracy_level_iso7(self) -> '_544.RollAngleRangeRelativeToAccuracy':
        '''RollAngleRangeRelativeToAccuracy: 'AccuracyLevelISO7' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_544.RollAngleRangeRelativeToAccuracy)(self.wrapped.AccuracyLevelISO7) if self.wrapped.AccuracyLevelISO7 else None

    @property
    def designed_gear(self) -> '_486.CylindricalCutterSimulatableGear':
        '''CylindricalCutterSimulatableGear: 'DesignedGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_486.CylindricalCutterSimulatableGear)(self.wrapped.DesignedGear) if self.wrapped.DesignedGear else None

    @property
    def shaver(self) -> '_515.CylindricalGearShaver':
        '''CylindricalGearShaver: 'Shaver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _515.CylindricalGearShaver.TYPE not in self.wrapped.Shaver.__class__.__mro__:
            raise CastException('Failed to cast shaver to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.Shaver.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaver.__class__)(self.wrapped.Shaver) if self.wrapped.Shaver else None

    @property
    def life_shaver(self) -> '_515.CylindricalGearShaver':
        '''CylindricalGearShaver: 'LifeShaver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _515.CylindricalGearShaver.TYPE not in self.wrapped.LifeShaver.__class__.__mro__:
            raise CastException('Failed to cast life_shaver to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.LifeShaver.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LifeShaver.__class__)(self.wrapped.LifeShaver) if self.wrapped.LifeShaver else None

    @property
    def new_cutter_start_of_shaving(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'NewCutterStartOfShaving' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.NewCutterStartOfShaving) if self.wrapped.NewCutterStartOfShaving else None

    @property
    def life_cutter_start_of_shaving(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'LifeCutterStartOfShaving' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.LifeCutterStartOfShaving) if self.wrapped.LifeCutterStartOfShaving else None

    @property
    def redressing_settings(self) -> 'List[_543.RedressingSettings[T]]':
        '''List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RedressingSettings, constructor.new(_543.RedressingSettings)[T])
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
