﻿'''_2071.py

FESubstructureWithSelectionForStaticAnalysis
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.utility.enums import _1549
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis.component_mode_synthesis import _203
from mastapy.nodal_analysis.dev_tools_analyses import _162
from mastapy.system_model.fe import _2077, _2067
from mastapy.math_utility.measured_vectors import _1326
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_WITH_SELECTION_FOR_STATIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureWithSelectionForStaticAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureWithSelectionForStaticAnalysis',)


class FESubstructureWithSelectionForStaticAnalysis(_2067.FESubstructureWithSelection):
    '''FESubstructureWithSelectionForStaticAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_SUBSTRUCTURE_WITH_SELECTION_FOR_STATIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FESubstructureWithSelectionForStaticAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def temperature_change_from_nominal(self) -> 'float':
        '''float: 'TemperatureChangeFromNominal' is the original name of this property.'''

        return self.wrapped.TemperatureChangeFromNominal

    @temperature_change_from_nominal.setter
    def temperature_change_from_nominal(self, value: 'float'):
        self.wrapped.TemperatureChangeFromNominal = float(value) if value else 0.0

    @property
    def contour_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption: 'ContourOption' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ContourOption, value) if self.wrapped.ContourOption else None

    @contour_option.setter
    def contour_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ContourOption = value

    @property
    def average_stress_to_nodes(self) -> 'bool':
        '''bool: 'AverageStressToNodes' is the original name of this property.'''

        return self.wrapped.AverageStressToNodes

    @average_stress_to_nodes.setter
    def average_stress_to_nodes(self, value: 'bool'):
        self.wrapped.AverageStressToNodes = bool(value) if value else False

    @property
    def full_fe_results(self) -> '_203.StaticCMSResults':
        '''StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_203.StaticCMSResults)(self.wrapped.FullFEResults) if self.wrapped.FullFEResults else None

    @property
    def static_draw_style(self) -> '_162.FEModelStaticAnalysisDrawStyle':
        '''FEModelStaticAnalysisDrawStyle: 'StaticDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_162.FEModelStaticAnalysisDrawStyle)(self.wrapped.StaticDrawStyle) if self.wrapped.StaticDrawStyle else None

    @property
    def boundary_conditions_selected_nodes(self) -> 'List[_2077.NodeBoundaryConditionStaticAnalysis]':
        '''List[NodeBoundaryConditionStaticAnalysis]: 'BoundaryConditionsSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsSelectedNodes, constructor.new(_2077.NodeBoundaryConditionStaticAnalysis))
        return value

    @property
    def boundary_conditions_all_nodes(self) -> 'List[_2077.NodeBoundaryConditionStaticAnalysis]':
        '''List[NodeBoundaryConditionStaticAnalysis]: 'BoundaryConditionsAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsAllNodes, constructor.new(_2077.NodeBoundaryConditionStaticAnalysis))
        return value

    @property
    def force_results(self) -> 'List[_1326.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'ForceResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ForceResults, constructor.new(_1326.VectorWithLinearAndAngularComponents))
        return value

    @property
    def displacement_results(self) -> 'List[_1326.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'DisplacementResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DisplacementResults, constructor.new(_1326.VectorWithLinearAndAngularComponents))
        return value

    def reset_forces(self):
        ''' 'ResetForces' is the original name of this method.'''

        self.wrapped.ResetForces()

    def reset_displacements(self):
        ''' 'ResetDisplacements' is the original name of this method.'''

        self.wrapped.ResetDisplacements()

    def torque_transfer_check(self):
        ''' 'TorqueTransferCheck' is the original name of this method.'''

        self.wrapped.TorqueTransferCheck()

    def solve(self):
        ''' 'Solve' is the original name of this method.'''

        self.wrapped.Solve()
