﻿'''_2030.py

UsedForExportingAnImportedFEsSetupOrSubstructuringStepToAnFEFile
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import list_with_selected_item, enum_with_selected_value
from mastapy.utility.units_and_measurements import _1173
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis.fe_export_utility import _1474
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_USED_FOR_EXPORTING_AN_IMPORTED_FES_SETUP_OR_SUBSTRUCTURING_STEP_TO_AN_FE_FILE = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'UsedForExportingAnImportedFEsSetupOrSubstructuringStepToAnFEFile')


__docformat__ = 'restructuredtext en'
__all__ = ('UsedForExportingAnImportedFEsSetupOrSubstructuringStepToAnFEFile',)


class UsedForExportingAnImportedFEsSetupOrSubstructuringStepToAnFEFile(_0.APIBase):
    '''UsedForExportingAnImportedFEsSetupOrSubstructuringStepToAnFEFile

    This is a mastapy class.
    '''

    TYPE = _USED_FOR_EXPORTING_AN_IMPORTED_FES_SETUP_OR_SUBSTRUCTURING_STEP_TO_AN_FE_FILE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UsedForExportingAnImportedFEsSetupOrSubstructuringStepToAnFEFile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_original_fe_file(self) -> 'bool':
        '''bool: 'IncludeOriginalFEFile' is the original name of this property.'''

        return self.wrapped.IncludeOriginalFEFile

    @include_original_fe_file.setter
    def include_original_fe_file(self, value: 'bool'):
        self.wrapped.IncludeOriginalFEFile = bool(value) if value else False

    @property
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(self) -> 'bool':
        '''bool: 'IncludeRigidCouplingNodesAndConstraintsAddedByMASTA' is the original name of this property.'''

        return self.wrapped.IncludeRigidCouplingNodesAndConstraintsAddedByMASTA

    @include_rigid_coupling_nodes_and_constraints_added_by_masta.setter
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(self, value: 'bool'):
        self.wrapped.IncludeRigidCouplingNodesAndConstraintsAddedByMASTA = bool(value) if value else False

    @property
    def include_reduction_commands(self) -> 'bool':
        '''bool: 'IncludeReductionCommands' is the original name of this property.'''

        return self.wrapped.IncludeReductionCommands

    @include_reduction_commands.setter
    def include_reduction_commands(self, value: 'bool'):
        self.wrapped.IncludeReductionCommands = bool(value) if value else False

    @property
    def length_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'LengthUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.LengthUnit) if self.wrapped.LengthUnit else None

    @length_unit.setter
    def length_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.LengthUnit = value

    @property
    def force_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'ForceUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.ForceUnit) if self.wrapped.ForceUnit else None

    @force_unit.setter
    def force_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ForceUnit = value

    @property
    def fe_package(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat':
        '''enum_with_selected_value.EnumWithSelectedValue_FEExportFormat: 'FEPackage' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.FEPackage, value) if self.wrapped.FEPackage else None

    @fe_package.setter
    def fe_package(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.FEPackage = value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def export_to_file(self, file_path: 'str'):
        ''' 'ExportToFile' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.ExportToFile(file_path if file_path else None)

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
