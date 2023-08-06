﻿'''_461.py

MountingError
'''


from typing import List

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MOUNTING_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'MountingError')


__docformat__ = 'restructuredtext en'
__all__ = ('MountingError',)


class MountingError(_0.APIBase):
    '''MountingError

    This is a mastapy class.
    '''

    TYPE = _MOUNTING_ERROR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountingError.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def first_section_radial_runout(self) -> 'float':
        '''float: 'FirstSectionRadialRunout' is the original name of this property.'''

        return self.wrapped.FirstSectionRadialRunout

    @first_section_radial_runout.setter
    def first_section_radial_runout(self, value: 'float'):
        self.wrapped.FirstSectionRadialRunout = float(value) if value else 0.0

    @property
    def second_section_radial_runout(self) -> 'float':
        '''float: 'SecondSectionRadialRunout' is the original name of this property.'''

        return self.wrapped.SecondSectionRadialRunout

    @second_section_radial_runout.setter
    def second_section_radial_runout(self, value: 'float'):
        self.wrapped.SecondSectionRadialRunout = float(value) if value else 0.0

    @property
    def first_section_phase_angle(self) -> 'float':
        '''float: 'FirstSectionPhaseAngle' is the original name of this property.'''

        return self.wrapped.FirstSectionPhaseAngle

    @first_section_phase_angle.setter
    def first_section_phase_angle(self, value: 'float'):
        self.wrapped.FirstSectionPhaseAngle = float(value) if value else 0.0

    @property
    def second_section_phase_angle(self) -> 'float':
        '''float: 'SecondSectionPhaseAngle' is the original name of this property.'''

        return self.wrapped.SecondSectionPhaseAngle

    @second_section_phase_angle.setter
    def second_section_phase_angle(self, value: 'float'):
        self.wrapped.SecondSectionPhaseAngle = float(value) if value else 0.0

    @property
    def distance_between_two_sections(self) -> 'float':
        '''float: 'DistanceBetweenTwoSections' is the original name of this property.'''

        return self.wrapped.DistanceBetweenTwoSections

    @distance_between_two_sections.setter
    def distance_between_two_sections(self, value: 'float'):
        self.wrapped.DistanceBetweenTwoSections = float(value) if value else 0.0

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
