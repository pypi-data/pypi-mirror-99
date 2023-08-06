﻿'''_1743.py

SKFModuleResults
'''


from typing import List

from mastapy.bearings.bearing_results.rolling.skf_module import (
    _1738, _1745, _1726, _1734,
    _1724, _1744, _1727, _1728,
    _1730
)
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SKF_MODULE_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'SKFModuleResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SKFModuleResults',)


class SKFModuleResults(_0.APIBase):
    '''SKFModuleResults

    This is a mastapy class.
    '''

    TYPE = _SKF_MODULE_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SKFModuleResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_load(self) -> '_1738.MinimumLoad':
        '''MinimumLoad: 'MinimumLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1738.MinimumLoad)(self.wrapped.MinimumLoad) if self.wrapped.MinimumLoad else None

    @property
    def viscosities(self) -> '_1745.Viscosities':
        '''Viscosities: 'Viscosities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1745.Viscosities)(self.wrapped.Viscosities) if self.wrapped.Viscosities else None

    @property
    def bearing_loads(self) -> '_1726.BearingLoads':
        '''BearingLoads: 'BearingLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1726.BearingLoads)(self.wrapped.BearingLoads) if self.wrapped.BearingLoads else None

    @property
    def grease_life_and_relubrication_interval(self) -> '_1734.GreaseLifeAndRelubricationInterval':
        '''GreaseLifeAndRelubricationInterval: 'GreaseLifeAndRelubricationInterval' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1734.GreaseLifeAndRelubricationInterval)(self.wrapped.GreaseLifeAndRelubricationInterval) if self.wrapped.GreaseLifeAndRelubricationInterval else None

    @property
    def adjusted_speed(self) -> '_1724.AdjustedSpeed':
        '''AdjustedSpeed: 'AdjustedSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1724.AdjustedSpeed)(self.wrapped.AdjustedSpeed) if self.wrapped.AdjustedSpeed else None

    @property
    def static_safety_factors(self) -> '_1744.StaticSafetyFactors':
        '''StaticSafetyFactors: 'StaticSafetyFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1744.StaticSafetyFactors)(self.wrapped.StaticSafetyFactors) if self.wrapped.StaticSafetyFactors else None

    @property
    def bearing_rating_life(self) -> '_1727.BearingRatingLife':
        '''BearingRatingLife: 'BearingRatingLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1727.BearingRatingLife)(self.wrapped.BearingRatingLife) if self.wrapped.BearingRatingLife else None

    @property
    def frequencies(self) -> '_1728.Frequencies':
        '''Frequencies: 'Frequencies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1728.Frequencies)(self.wrapped.Frequencies) if self.wrapped.Frequencies else None

    @property
    def friction(self) -> '_1730.Friction':
        '''Friction: 'Friction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1730.Friction)(self.wrapped.Friction) if self.wrapped.Friction else None

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
