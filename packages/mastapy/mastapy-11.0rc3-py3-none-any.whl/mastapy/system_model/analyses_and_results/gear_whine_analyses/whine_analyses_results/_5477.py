﻿'''_5477.py

ResultNodeSelection
'''


from typing import Callable, List

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RESULT_NODE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'ResultNodeSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultNodeSelection',)


class ResultNodeSelection(_0.APIBase):
    '''ResultNodeSelection

    This is a mastapy class.
    '''

    TYPE = _RESULT_NODE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultNodeSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_shown(self) -> 'bool':
        '''bool: 'IsShown' is the original name of this property.'''

        return self.wrapped.IsShown

    @is_shown.setter
    def is_shown(self, value: 'bool'):
        self.wrapped.IsShown = bool(value) if value else False

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def add_to_selected_group(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddToSelectedGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddToSelectedGroup

    @property
    def remove_from_selected_group(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'RemoveFromSelectedGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveFromSelectedGroup

    @property
    def is_in_selected_group(self) -> 'bool':
        '''bool: 'IsInSelectedGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsInSelectedGroup

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
