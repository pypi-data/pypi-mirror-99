﻿'''_1723.py

ISO762006Results
'''


from typing import List

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ISO762006_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults', 'ISO762006Results')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO762006Results',)


class ISO762006Results(_0.APIBase):
    '''ISO762006Results

    This is a mastapy class.
    '''

    TYPE = _ISO762006_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO762006Results.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def static_equivalent_load(self) -> 'float':
        '''float: 'StaticEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticEquivalentLoad

    @property
    def safety_factor(self) -> 'float':
        '''float: 'SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SafetyFactor

    @property
    def recommended_maximum_element_normal_stress(self) -> 'float':
        '''float: 'RecommendedMaximumElementNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RecommendedMaximumElementNormalStress

    @property
    def static_axial_load_factor(self) -> 'float':
        '''float: 'StaticAxialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticAxialLoadFactor

    @property
    def static_radial_load_factor(self) -> 'float':
        '''float: 'StaticRadialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticRadialLoadFactor

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
