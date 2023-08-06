﻿'''_462.py

ProcessCalculation
'''


from typing import Callable, List

from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _467, _454, _481
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PROCESS_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessCalculation',)


class ProcessCalculation(_0.APIBase):
    '''ProcessCalculation

    This is a mastapy class.
    '''

    TYPE = _PROCESS_CALCULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculate_modifications(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateModifications

    @property
    def calculate_left_modifications(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateLeftModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateLeftModifications

    @property
    def calculate_right_modifications(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateRightModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateRightModifications

    @property
    def calculate_left_total_modifications(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateLeftTotalModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateLeftTotalModifications

    @property
    def calculate_right_total_modifications(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateRightTotalModifications' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateRightTotalModifications

    @property
    def calculate_idle_distance(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateIdleDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateIdleDistance

    @property
    def calculate_maximum_shaft_mark_length(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateMaximumShaftMarkLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateMaximumShaftMarkLength

    @property
    def calculate_shaft_mark(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateShaftMark' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateShaftMark

    @property
    def shaft_mark_length(self) -> 'float':
        '''float: 'ShaftMarkLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaftMarkLength

    @property
    def idle_distance(self) -> 'float':
        '''float: 'IdleDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IdleDistance

    @property
    def centre_distance_parabolic_parameter(self) -> 'float':
        '''float: 'CentreDistanceParabolicParameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CentreDistanceParabolicParameter

    @property
    def cutter_minimum_effective_length(self) -> 'float':
        '''float: 'CutterMinimumEffectiveLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterMinimumEffectiveLength

    @property
    def minimum_allowable_neck_width(self) -> 'float':
        '''float: 'MinimumAllowableNeckWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumAllowableNeckWidth

    @property
    def neck_width(self) -> 'float':
        '''float: 'NeckWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NeckWidth

    @property
    def cutter_gear_rotation_ratio(self) -> 'float':
        '''float: 'CutterGearRotationRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterGearRotationRatio

    @property
    def centre_distance(self) -> 'float':
        '''float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CentreDistance

    @property
    def shaft_angle(self) -> 'float':
        '''float: 'ShaftAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaftAngle

    @property
    def setting_angle(self) -> 'float':
        '''float: 'SettingAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SettingAngle

    @property
    def inputs(self) -> '_467.ProcessSimulationInput':
        '''ProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _467.ProcessSimulationInput.TYPE not in self.wrapped.Inputs.__class__.__mro__:
            raise CastException('Failed to cast inputs to ProcessSimulationInput. Expected: {}.'.format(self.wrapped.Inputs.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Inputs.__class__)(self.wrapped.Inputs) if self.wrapped.Inputs else None

    @property
    def inputs_of_type_hobbing_process_simulation_input(self) -> '_454.HobbingProcessSimulationInput':
        '''HobbingProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _454.HobbingProcessSimulationInput.TYPE not in self.wrapped.Inputs.__class__.__mro__:
            raise CastException('Failed to cast inputs to HobbingProcessSimulationInput. Expected: {}.'.format(self.wrapped.Inputs.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Inputs.__class__)(self.wrapped.Inputs) if self.wrapped.Inputs else None

    @property
    def inputs_of_type_worm_grinding_process_simulation_input(self) -> '_481.WormGrindingProcessSimulationInput':
        '''WormGrindingProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _481.WormGrindingProcessSimulationInput.TYPE not in self.wrapped.Inputs.__class__.__mro__:
            raise CastException('Failed to cast inputs to WormGrindingProcessSimulationInput. Expected: {}.'.format(self.wrapped.Inputs.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Inputs.__class__)(self.wrapped.Inputs) if self.wrapped.Inputs else None

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
