﻿'''_83.py

SNCurve
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.materials import _84
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SN_CURVE = python_net_import('SMT.MastaAPI.Materials', 'SNCurve')


__docformat__ = 'restructuredtext en'
__all__ = ('SNCurve',)


class SNCurve(_0.APIBase):
    '''SNCurve

    This is a mastapy class.
    '''

    TYPE = _SN_CURVE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SNCurve.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_cycles_for_static_stress(self) -> 'float':
        '''float: 'MaximumCyclesForStaticStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumCyclesForStaticStress

    @property
    def cycles_for_infinite_life(self) -> 'float':
        '''float: 'CyclesForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CyclesForInfiniteLife

    @property
    def fatigue_limit_for_infinite_life(self) -> 'float':
        '''float: 'FatigueLimitForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FatigueLimitForInfiniteLife

    @property
    def stress_for_first_cycle_failure(self) -> 'float':
        '''float: 'StressForFirstCycleFailure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StressForFirstCycleFailure

    @property
    def points(self) -> 'List[_84.SNCurvePoint]':
        '''List[SNCurvePoint]: 'Points' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Points, constructor.new(_84.SNCurvePoint))
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
