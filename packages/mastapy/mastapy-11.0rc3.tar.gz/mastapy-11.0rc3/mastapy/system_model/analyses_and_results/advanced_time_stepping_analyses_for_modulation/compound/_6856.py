﻿'''_6856.py

MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model import _2140
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6727
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6902
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation',)


class MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation(_6902.VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2140.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2140.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6727.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6727.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6727.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6727.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation))
        return value
