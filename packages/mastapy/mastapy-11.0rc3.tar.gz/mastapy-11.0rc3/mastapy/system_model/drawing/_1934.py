﻿'''_1934.py

RotorDynamicsViewable
'''


from typing import List

from mastapy.system_model.analyses_and_results.rotor_dynamics import _3690
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3274
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _3535
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6221
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ROTOR_DYNAMICS_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'RotorDynamicsViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('RotorDynamicsViewable',)


class RotorDynamicsViewable(_0.APIBase):
    '''RotorDynamicsViewable

    This is a mastapy class.
    '''

    TYPE = _ROTOR_DYNAMICS_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RotorDynamicsViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rotor_dynamics(self) -> '_3690.RotorDynamicsDrawStyle':
        '''RotorDynamicsDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3690.RotorDynamicsDrawStyle.TYPE not in self.wrapped.RotorDynamics.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to RotorDynamicsDrawStyle. Expected: {}.'.format(self.wrapped.RotorDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RotorDynamics.__class__)(self.wrapped.RotorDynamics) if self.wrapped.RotorDynamics else None

    @property
    def rotor_dynamics_of_type_steady_state_synchronous_response_draw_style(self) -> '_3274.SteadyStateSynchronousResponseDrawStyle':
        '''SteadyStateSynchronousResponseDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3274.SteadyStateSynchronousResponseDrawStyle.TYPE not in self.wrapped.RotorDynamics.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to SteadyStateSynchronousResponseDrawStyle. Expected: {}.'.format(self.wrapped.RotorDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RotorDynamics.__class__)(self.wrapped.RotorDynamics) if self.wrapped.RotorDynamics else None

    @property
    def rotor_dynamics_of_type_stability_analysis_draw_style(self) -> '_3535.StabilityAnalysisDrawStyle':
        '''StabilityAnalysisDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3535.StabilityAnalysisDrawStyle.TYPE not in self.wrapped.RotorDynamics.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to StabilityAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.RotorDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RotorDynamics.__class__)(self.wrapped.RotorDynamics) if self.wrapped.RotorDynamics else None

    @property
    def rotor_dynamics_of_type_critical_speed_analysis_draw_style(self) -> '_6221.CriticalSpeedAnalysisDrawStyle':
        '''CriticalSpeedAnalysisDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6221.CriticalSpeedAnalysisDrawStyle.TYPE not in self.wrapped.RotorDynamics.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to CriticalSpeedAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.RotorDynamics.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RotorDynamics.__class__)(self.wrapped.RotorDynamics) if self.wrapped.RotorDynamics else None

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
