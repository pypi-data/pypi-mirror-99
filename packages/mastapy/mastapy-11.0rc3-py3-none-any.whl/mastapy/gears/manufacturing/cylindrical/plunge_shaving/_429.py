﻿'''_429.py

PlungeShaverCalculation
'''


from typing import List

from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _430, _439
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverCalculation',)


class PlungeShaverCalculation(_0.APIBase):
    '''PlungeShaverCalculation

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_CALCULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def inputs(self) -> '_430.PlungeShaverCalculationInputs':
        '''PlungeShaverCalculationInputs: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_430.PlungeShaverCalculationInputs)(self.wrapped.Inputs) if self.wrapped.Inputs else None

    @property
    def simulation_of_ideal_shaver_conjugate_to_the_designed_gear(self) -> '_439.VirtualPlungeShaverOutputs':
        '''VirtualPlungeShaverOutputs: 'SimulationOfIdealShaverConjugateToTheDesignedGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_439.VirtualPlungeShaverOutputs)(self.wrapped.SimulationOfIdealShaverConjugateToTheDesignedGear) if self.wrapped.SimulationOfIdealShaverConjugateToTheDesignedGear else None

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
