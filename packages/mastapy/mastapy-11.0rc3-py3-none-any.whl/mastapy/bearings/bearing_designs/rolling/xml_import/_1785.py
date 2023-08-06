﻿'''_1785.py

RollingBearingImporter
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_designs.rolling.xml_import import _1786
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ROLLING_BEARING_IMPORTER = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport', 'RollingBearingImporter')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearingImporter',)


class RollingBearingImporter(_0.APIBase):
    '''RollingBearingImporter

    This is a mastapy class.
    '''

    TYPE = _ROLLING_BEARING_IMPORTER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingBearingImporter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def replace_existing_bearings(self) -> 'bool':
        '''bool: 'ReplaceExistingBearings' is the original name of this property.'''

        return self.wrapped.ReplaceExistingBearings

    @replace_existing_bearings.setter
    def replace_existing_bearings(self, value: 'bool'):
        self.wrapped.ReplaceExistingBearings = bool(value) if value else False

    @property
    def open_files_in_directory(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'OpenFilesInDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OpenFilesInDirectory

    @property
    def import_all(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ImportAll' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportAll

    @property
    def number_of_bearings_ready_to_import(self) -> 'int':
        '''int: 'NumberOfBearingsReadyToImport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfBearingsReadyToImport

    @property
    def save_setup(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SaveSetup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SaveSetup

    @property
    def load_setup(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'LoadSetup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadSetup

    @property
    def reset_to_defaults(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ResetToDefaults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResetToDefaults

    @property
    def mappings(self) -> 'List[_1786.XmlBearingTypeMapping]':
        '''List[XmlBearingTypeMapping]: 'Mappings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Mappings, constructor.new(_1786.XmlBearingTypeMapping))
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
