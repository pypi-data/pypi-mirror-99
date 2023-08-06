﻿'''_1524.py

FullFEModel
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses import _1481
from mastapy.nodal_analysis.component_mode_synthesis import _1522, _1519
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FULL_FE_MODEL = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'FullFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('FullFEModel',)


class FullFEModel(_0.APIBase):
    '''FullFEModel

    This is a mastapy class.
    '''

    TYPE = _FULL_FE_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FullFEModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def memory_required_for_stiffness_and_mass_matrices(self) -> 'str':
        '''str: 'MemoryRequiredForStiffnessAndMassMatrices' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MemoryRequiredForStiffnessAndMassMatrices

    @property
    def memory_required_for_displacement_expansion(self) -> 'str':
        '''str: 'MemoryRequiredForDisplacementExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MemoryRequiredForDisplacementExpansion

    @property
    def total_memory_required_for_mesh(self) -> 'str':
        '''str: 'TotalMemoryRequiredForMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryRequiredForMesh

    @property
    def total_memory_required_for_results(self) -> 'str':
        '''str: 'TotalMemoryRequiredForResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryRequiredForResults

    @property
    def estimated_memory_required_for_stiffness_and_mass_matrices(self) -> 'str':
        '''str: 'EstimatedMemoryRequiredForStiffnessAndMassMatrices' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EstimatedMemoryRequiredForStiffnessAndMassMatrices

    @property
    def estimated_memory_required_for_displacement_expansion(self) -> 'str':
        '''str: 'EstimatedMemoryRequiredForDisplacementExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EstimatedMemoryRequiredForDisplacementExpansion

    @property
    def estimated_total_memory_required_for_results(self) -> 'str':
        '''str: 'EstimatedTotalMemoryRequiredForResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EstimatedTotalMemoryRequiredForResults

    @property
    def time_taken_for_reduction(self) -> 'str':
        '''str: 'TimeTakenForReduction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TimeTakenForReduction

    @property
    def specifications_of_computer_used_for_reduction(self) -> 'str':
        '''str: 'SpecificationsOfComputerUsedForReduction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpecificationsOfComputerUsedForReduction

    @property
    def masta_version_used_for_reduction(self) -> 'str':
        '''str: 'MASTAVersionUsedForReduction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MASTAVersionUsedForReduction

    @property
    def has_condensation_result(self) -> 'bool':
        '''bool: 'HasCondensationResult' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasCondensationResult

    @property
    def fe_model(self) -> '_1481.FEModel':
        '''FEModel: 'FEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1481.FEModel)(self.wrapped.FEModel) if self.wrapped.FEModel else None

    @property
    def reduction_options(self) -> '_1522.CMSOptions':
        '''CMSOptions: 'ReductionOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1522.CMSOptions)(self.wrapped.ReductionOptions) if self.wrapped.ReductionOptions else None

    @property
    def element_face_groups(self) -> 'List[_1519.CMSElementFaceGroup]':
        '''List[CMSElementFaceGroup]: 'ElementFaceGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElementFaceGroups, constructor.new(_1519.CMSElementFaceGroup))
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
