﻿'''_837.py

ChartInfoBase
'''


from typing import List, Generic, TypeVar

from PIL.Image import Image

from mastapy.math_utility.optimisation import _1313
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility.reporting_property_framework import _1479
from mastapy.gears.gear_set_pareto_optimiser import (
    _839, _838, _841, _845,
    _846, _849, _852, _871,
    _872, _835, _847
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy.gears.analysis import _1125
from mastapy._internal.python_net import python_net_import

_CHART_INFO_BASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ChartInfoBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ChartInfoBase',)


TAnalysis = TypeVar('TAnalysis', bound='_1125.AbstractGearSetAnalysis')
TCandidate = TypeVar('TCandidate')


class ChartInfoBase(_0.APIBase, Generic[TAnalysis, TCandidate]):
    '''ChartInfoBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    '''

    TYPE = _CHART_INFO_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ChartInfoBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def select_chart_type(self) -> '_1313.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart':
        '''ParetoOptimisationStrategyChartInformation.ScatterOrBarChart: 'SelectChartType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SelectChartType)
        return constructor.new(_1313.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart)(value) if value else None

    @select_chart_type.setter
    def select_chart_type(self, value: '_1313.ParetoOptimisationStrategyChartInformation.ScatterOrBarChart'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SelectChartType = value

    @property
    def chart_type(self) -> '_1479.CustomChartType':
        '''CustomChartType: 'ChartType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ChartType)
        return constructor.new(_1479.CustomChartType)(value) if value else None

    @property
    def selected_candidate_design(self) -> 'int':
        '''int: 'SelectedCandidateDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectedCandidateDesign

    @property
    def result_chart_scatter(self) -> 'Image':
        '''Image: 'ResultChartScatter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ResultChartScatter)
        return value

    @property
    def result_chart_bar_and_line(self) -> 'Image':
        '''Image: 'ResultChartBarAndLine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.ResultChartBarAndLine)
        return value

    @property
    def chart_name(self) -> 'str':
        '''str: 'ChartName' is the original name of this property.'''

        return self.wrapped.ChartName

    @chart_name.setter
    def chart_name(self, value: 'str'):
        self.wrapped.ChartName = str(value) if value else None

    @property
    def optimiser(self) -> '_839.DesignSpaceSearchBase[TAnalysis, TCandidate]':
        '''DesignSpaceSearchBase[TAnalysis, TCandidate]: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _839.DesignSpaceSearchBase[TAnalysis, TCandidate].TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to DesignSpaceSearchBase[TAnalysis, TCandidate]. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_cylindrical_gear_set_pareto_optimiser(self) -> '_838.CylindricalGearSetParetoOptimiser':
        '''CylindricalGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _838.CylindricalGearSetParetoOptimiser.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to CylindricalGearSetParetoOptimiser. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_face_gear_set_pareto_optimiser(self) -> '_841.FaceGearSetParetoOptimiser':
        '''FaceGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _841.FaceGearSetParetoOptimiser.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to FaceGearSetParetoOptimiser. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_gear_set_pareto_optimiser(self) -> '_845.GearSetParetoOptimiser':
        '''GearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _845.GearSetParetoOptimiser.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to GearSetParetoOptimiser. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_hypoid_gear_set_pareto_optimiser(self) -> '_846.HypoidGearSetParetoOptimiser':
        '''HypoidGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _846.HypoidGearSetParetoOptimiser.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to HypoidGearSetParetoOptimiser. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_micro_geometry_design_space_search(self) -> '_849.MicroGeometryDesignSpaceSearch':
        '''MicroGeometryDesignSpaceSearch: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _849.MicroGeometryDesignSpaceSearch.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to MicroGeometryDesignSpaceSearch. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_micro_geometry_gear_set_design_space_search(self) -> '_852.MicroGeometryGearSetDesignSpaceSearch':
        '''MicroGeometryGearSetDesignSpaceSearch: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _852.MicroGeometryGearSetDesignSpaceSearch.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to MicroGeometryGearSetDesignSpaceSearch. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_spiral_bevel_gear_set_pareto_optimiser(self) -> '_871.SpiralBevelGearSetParetoOptimiser':
        '''SpiralBevelGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _871.SpiralBevelGearSetParetoOptimiser.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to SpiralBevelGearSetParetoOptimiser. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_straight_bevel_gear_set_pareto_optimiser(self) -> '_872.StraightBevelGearSetParetoOptimiser':
        '''StraightBevelGearSetParetoOptimiser: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _872.StraightBevelGearSetParetoOptimiser.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to StraightBevelGearSetParetoOptimiser. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def bars(self) -> 'List[_835.BarForPareto[TAnalysis, TCandidate]]':
        '''List[BarForPareto[TAnalysis, TCandidate]]: 'Bars' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bars, constructor.new(_835.BarForPareto)[TAnalysis, TCandidate])
        return value

    @property
    def input_sliders(self) -> 'List[_847.InputSliderForPareto[TAnalysis, TCandidate]]':
        '''List[InputSliderForPareto[TAnalysis, TCandidate]]: 'InputSliders' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InputSliders, constructor.new(_847.InputSliderForPareto)[TAnalysis, TCandidate])
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def remove_chart(self):
        ''' 'RemoveChart' is the original name of this method.'''

        self.wrapped.RemoveChart()

    def add_bar(self):
        ''' 'AddBar' is the original name of this method.'''

        self.wrapped.AddBar()

    def add_selected_design(self):
        ''' 'AddSelectedDesign' is the original name of this method.'''

        self.wrapped.AddSelectedDesign()

    def add_selected_designs(self):
        ''' 'AddSelectedDesigns' is the original name of this method.'''

        self.wrapped.AddSelectedDesigns()

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
