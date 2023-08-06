﻿'''_2016.py

NodeBoundaryConditionStaticAnalysis
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes import _1980, _1979
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_NODE_BOUNDARY_CONDITION_STATIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'NodeBoundaryConditionStaticAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeBoundaryConditionStaticAnalysis',)


class NodeBoundaryConditionStaticAnalysis(_0.APIBase):
    '''NodeBoundaryConditionStaticAnalysis

    This is a mastapy class.
    '''

    TYPE = _NODE_BOUNDARY_CONDITION_STATIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodeBoundaryConditionStaticAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def ground_all_degrees_of_freedom(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'GroundAllDegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GroundAllDegreesOfFreedom

    @property
    def boundary_conditions_linear(self) -> 'List[_1980.DegreeOfFreedomBoundaryConditionLinear]':
        '''List[DegreeOfFreedomBoundaryConditionLinear]: 'BoundaryConditionsLinear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsLinear, constructor.new(_1980.DegreeOfFreedomBoundaryConditionLinear))
        return value

    @property
    def boundary_conditions_angular(self) -> 'List[_1979.DegreeOfFreedomBoundaryConditionAngular]':
        '''List[DegreeOfFreedomBoundaryConditionAngular]: 'BoundaryConditionsAngular' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsAngular, constructor.new(_1979.DegreeOfFreedomBoundaryConditionAngular))
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
