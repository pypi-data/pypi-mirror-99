﻿'''_1839.py

DutyCycleImporter
'''


from typing import List

from mastapy.system_model import _1843, _1840
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2072, _2071
from mastapy.system_model.analyses_and_results.load_case_groups import _5303
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_IMPORTER = python_net_import('SMT.MastaAPI.SystemModel', 'DutyCycleImporter')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleImporter',)


class DutyCycleImporter(_0.APIBase):
    '''DutyCycleImporter

    This is a mastapy class.
    '''

    TYPE = _DUTY_CYCLE_IMPORTER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DutyCycleImporter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycles_to_import(self) -> 'List[_1843.IncludeDutyCycleOption]':
        '''List[IncludeDutyCycleOption]: 'DutyCyclesToImport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DutyCyclesToImport, constructor.new(_1843.IncludeDutyCycleOption))
        return value

    @property
    def power_load_destinations(self) -> 'List[_1840.DutyCycleImporterDesignEntityMatch[_2072.PowerLoad]]':
        '''List[DutyCycleImporterDesignEntityMatch[PowerLoad]]: 'PowerLoadDestinations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoadDestinations, constructor.new(_1840.DutyCycleImporterDesignEntityMatch)[_2072.PowerLoad])
        return value

    @property
    def point_load_destinations(self) -> 'List[_1840.DutyCycleImporterDesignEntityMatch[_2071.PointLoad]]':
        '''List[DutyCycleImporterDesignEntityMatch[PointLoad]]: 'PointLoadDestinations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoadDestinations, constructor.new(_1840.DutyCycleImporterDesignEntityMatch)[_2071.PointLoad])
        return value

    @property
    def design_state_destinations(self) -> 'List[_1840.DutyCycleImporterDesignEntityMatch[_5303.DesignState]]':
        '''List[DutyCycleImporterDesignEntityMatch[DesignState]]: 'DesignStateDestinations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignStateDestinations, constructor.new(_1840.DutyCycleImporterDesignEntityMatch)[_5303.DesignState])
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
