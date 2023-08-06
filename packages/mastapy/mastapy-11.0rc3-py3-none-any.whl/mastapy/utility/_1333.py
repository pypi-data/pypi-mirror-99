﻿'''_1333.py

DispatcherHelper
'''


from typing import List

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DISPATCHER_HELPER = python_net_import('SMT.MastaAPI.Utility', 'DispatcherHelper')


__docformat__ = 'restructuredtext en'
__all__ = ('DispatcherHelper',)


class DispatcherHelper(_0.APIBase):
    '''DispatcherHelper

    This is a mastapy class.
    '''

    TYPE = _DISPATCHER_HELPER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DispatcherHelper.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_suspended(self) -> 'bool':
        '''bool: 'IsSuspended' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsSuspended

    @property
    def disable_processing_count(self) -> 'int':
        '''int: 'DisableProcessingCount' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisableProcessingCount

    @property
    def frame_depth(self) -> 'int':
        '''int: 'FrameDepth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FrameDepth

    @property
    def timers(self) -> 'str':
        '''str: 'Timers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Timers

    @property
    def number_of_queued_items(self) -> 'int':
        '''int: 'NumberOfQueuedItems' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfQueuedItems

    @property
    def has_shutdown_started(self) -> 'bool':
        '''bool: 'HasShutdownStarted' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasShutdownStarted

    @property
    def has_shutdown_finished(self) -> 'bool':
        '''bool: 'HasShutdownFinished' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasShutdownFinished

    @property
    def thread(self) -> 'str':
        '''str: 'Thread' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Thread

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
