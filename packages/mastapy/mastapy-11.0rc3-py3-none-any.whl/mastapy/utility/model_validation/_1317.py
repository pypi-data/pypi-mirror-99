﻿'''_1317.py

StatusItem
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.utility.model_validation import _1314
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_STATUS_ITEM = python_net_import('SMT.MastaAPI.Utility.ModelValidation', 'StatusItem')


__docformat__ = 'restructuredtext en'
__all__ = ('StatusItem',)


class StatusItem(_0.APIBase):
    '''StatusItem

    This is a mastapy class.
    '''

    TYPE = _STATUS_ITEM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StatusItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def description(self) -> 'str':
        '''str: 'Description' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Description

    @property
    def can_fix(self) -> 'bool':
        '''bool: 'CanFix' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CanFix

    @property
    def fixes(self) -> 'List[_1314.Fix]':
        '''List[Fix]: 'Fixes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Fixes, constructor.new(_1314.Fix))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def apply_first_fix(self):
        ''' 'ApplyFirstFix' is the original name of this method.'''

        self.wrapped.ApplyFirstFix()

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
