﻿'''_4054.py

ParametricStudyVariable
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4045, _4042
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results import _2322
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_VARIABLE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyVariable')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyVariable',)


class ParametricStudyVariable(_2322.AnalysisCaseVariable):
    '''ParametricStudyVariable

    This is a mastapy class.
    '''

    TYPE = _PARAMETRIC_STUDY_VARIABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParametricStudyVariable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def parameter_name(self) -> 'str':
        '''str: 'ParameterName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ParameterName

    @property
    def dimension(self) -> '_4045.ParametricStudyDimension':
        '''ParametricStudyDimension: 'Dimension' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Dimension)
        return constructor.new(_4045.ParametricStudyDimension)(value) if value else None

    @dimension.setter
    def dimension(self, value: '_4045.ParametricStudyDimension'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Dimension = value

    @property
    def distribution(self) -> '_4042.MonteCarloDistribution':
        '''MonteCarloDistribution: 'Distribution' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Distribution)
        return constructor.new(_4042.MonteCarloDistribution)(value) if value else None

    @distribution.setter
    def distribution(self, value: '_4042.MonteCarloDistribution'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Distribution = value

    @property
    def standard_deviation(self) -> 'float':
        '''float: 'StandardDeviation' is the original name of this property.'''

        return self.wrapped.StandardDeviation

    @standard_deviation.setter
    def standard_deviation(self, value: 'float'):
        self.wrapped.StandardDeviation = float(value) if value else 0.0

    @property
    def unit(self) -> 'str':
        '''str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Unit

    @property
    def mean_value(self) -> 'float':
        '''float: 'MeanValue' is the original name of this property.'''

        return self.wrapped.MeanValue

    @mean_value.setter
    def mean_value(self, value: 'float'):
        self.wrapped.MeanValue = float(value) if value else 0.0

    @property
    def start_value(self) -> 'float':
        '''float: 'StartValue' is the original name of this property.'''

        return self.wrapped.StartValue

    @start_value.setter
    def start_value(self, value: 'float'):
        self.wrapped.StartValue = float(value) if value else 0.0

    @property
    def end_value(self) -> 'float':
        '''float: 'EndValue' is the original name of this property.'''

        return self.wrapped.EndValue

    @end_value.setter
    def end_value(self, value: 'float'):
        self.wrapped.EndValue = float(value) if value else 0.0

    @property
    def maximum_value(self) -> 'float':
        '''float: 'MaximumValue' is the original name of this property.'''

        return self.wrapped.MaximumValue

    @maximum_value.setter
    def maximum_value(self, value: 'float'):
        self.wrapped.MaximumValue = float(value) if value else 0.0

    @property
    def minimum_value(self) -> 'float':
        '''float: 'MinimumValue' is the original name of this property.'''

        return self.wrapped.MinimumValue

    @minimum_value.setter
    def minimum_value(self, value: 'float'):
        self.wrapped.MinimumValue = float(value) if value else 0.0

    @property
    def current_values(self) -> 'str':
        '''str: 'CurrentValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CurrentValues

    @property
    def group(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'Group' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.Group) if self.wrapped.Group else None

    @group.setter
    def group(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.Group = value

    @property
    def show_variable_on_axis(self) -> 'bool':
        '''bool: 'ShowVariableOnAxis' is the original name of this property.'''

        return self.wrapped.ShowVariableOnAxis

    @show_variable_on_axis.setter
    def show_variable_on_axis(self, value: 'bool'):
        self.wrapped.ShowVariableOnAxis = bool(value) if value else False

    def set_values(self):
        ''' 'SetValues' is the original name of this method.'''

        self.wrapped.SetValues()

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()

    def up(self):
        ''' 'Up' is the original name of this method.'''

        self.wrapped.Up()

    def down(self):
        ''' 'Down' is the original name of this method.'''

        self.wrapped.Down()
