﻿'''_1783.py

BearingProtection
'''


from typing import List

from mastapy.bearings.bearing_designs.rolling import _1785
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEARING_PROTECTION = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BearingProtection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingProtection',)


class BearingProtection(_0.APIBase):
    '''BearingProtection

    This is a mastapy class.
    '''

    TYPE = _BEARING_PROTECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingProtection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def protection_level(self) -> '_1785.BearingProtectionLevel':
        '''BearingProtectionLevel: 'ProtectionLevel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ProtectionLevel)
        return constructor.new(_1785.BearingProtectionLevel)(value) if value else None

    @property
    def bearing_is_protected(self) -> 'bool':
        '''bool: 'BearingIsProtected' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BearingIsProtected

    @property
    def internal_geometry_hidden(self) -> 'str':
        '''str: 'InternalGeometryHidden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InternalGeometryHidden

    @property
    def advanced_bearing_results_hidden(self) -> 'str':
        '''str: 'AdvancedBearingResultsHidden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AdvancedBearingResultsHidden

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
