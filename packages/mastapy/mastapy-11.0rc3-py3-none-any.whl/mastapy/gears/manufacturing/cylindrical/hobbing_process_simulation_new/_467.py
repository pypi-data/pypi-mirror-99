﻿'''_467.py

ProcessSimulationInput
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _445, _441, _472, _447,
    _446
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PROCESS_SIMULATION_INPUT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessSimulationInput')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessSimulationInput',)


class ProcessSimulationInput(_0.APIBase):
    '''ProcessSimulationInput

    This is a mastapy class.
    '''

    TYPE = _PROCESS_SIMULATION_INPUT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessSimulationInput.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def start_height_above_the_gear_center(self) -> 'float':
        '''float: 'StartHeightAboveTheGearCenter' is the original name of this property.'''

        return self.wrapped.StartHeightAboveTheGearCenter

    @start_height_above_the_gear_center.setter
    def start_height_above_the_gear_center(self, value: 'float'):
        self.wrapped.StartHeightAboveTheGearCenter = float(value) if value else 0.0

    @property
    def feed(self) -> 'float':
        '''float: 'Feed' is the original name of this property.'''

        return self.wrapped.Feed

    @feed.setter
    def feed(self, value: 'float'):
        self.wrapped.Feed = float(value) if value else 0.0

    @property
    def centre_distance_offset_specification_method(self) -> '_445.CentreDistanceOffsetMethod':
        '''CentreDistanceOffsetMethod: 'CentreDistanceOffsetSpecificationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CentreDistanceOffsetSpecificationMethod)
        return constructor.new(_445.CentreDistanceOffsetMethod)(value) if value else None

    @centre_distance_offset_specification_method.setter
    def centre_distance_offset_specification_method(self, value: '_445.CentreDistanceOffsetMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CentreDistanceOffsetSpecificationMethod = value

    @property
    def centre_distance_offset(self) -> 'float':
        '''float: 'CentreDistanceOffset' is the original name of this property.'''

        return self.wrapped.CentreDistanceOffset

    @centre_distance_offset.setter
    def centre_distance_offset(self, value: 'float'):
        self.wrapped.CentreDistanceOffset = float(value) if value else 0.0

    @property
    def gear_design_lead_crown_modification(self) -> 'float':
        '''float: 'GearDesignLeadCrownModification' is the original name of this property.'''

        return self.wrapped.GearDesignLeadCrownModification

    @gear_design_lead_crown_modification.setter
    def gear_design_lead_crown_modification(self, value: 'float'):
        self.wrapped.GearDesignLeadCrownModification = float(value) if value else 0.0

    @property
    def gear_designed_lead_crown_length(self) -> 'float':
        '''float: 'GearDesignedLeadCrownLength' is the original name of this property.'''

        return self.wrapped.GearDesignedLeadCrownLength

    @gear_designed_lead_crown_length.setter
    def gear_designed_lead_crown_length(self, value: 'float'):
        self.wrapped.GearDesignedLeadCrownLength = float(value) if value else 0.0

    @property
    def analysis_setting(self) -> '_441.AnalysisMethod':
        '''AnalysisMethod: 'AnalysisSetting' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AnalysisSetting)
        return constructor.new(_441.AnalysisMethod)(value) if value else None

    @analysis_setting.setter
    def analysis_setting(self, value: '_441.AnalysisMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AnalysisSetting = value

    @property
    def shaft_angle_offset(self) -> 'float':
        '''float: 'ShaftAngleOffset' is the original name of this property.'''

        return self.wrapped.ShaftAngleOffset

    @shaft_angle_offset.setter
    def shaft_angle_offset(self, value: 'float'):
        self.wrapped.ShaftAngleOffset = float(value) if value else 0.0

    @property
    def tooth_index(self) -> 'int':
        '''int: 'ToothIndex' is the original name of this property.'''

        return self.wrapped.ToothIndex

    @tooth_index.setter
    def tooth_index(self, value: 'int'):
        self.wrapped.ToothIndex = int(value) if value else 0

    @property
    def cutter_mounting_error(self) -> '_472.RackMountingError':
        '''RackMountingError: 'CutterMountingError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_472.RackMountingError)(self.wrapped.CutterMountingError) if self.wrapped.CutterMountingError else None

    @property
    def gear_mounting_error(self) -> '_447.GearMountingError':
        '''GearMountingError: 'GearMountingError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_447.GearMountingError)(self.wrapped.GearMountingError) if self.wrapped.GearMountingError else None

    @property
    def cutter_head_slide_error(self) -> '_446.CutterHeadSlideError':
        '''CutterHeadSlideError: 'CutterHeadSlideError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_446.CutterHeadSlideError)(self.wrapped.CutterHeadSlideError) if self.wrapped.CutterHeadSlideError else None

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
