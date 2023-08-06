﻿'''_6831.py

DatumCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6701
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6805
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'DatumCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundAdvancedTimeSteppingAnalysisForModulation',)


class DatumCompoundAdvancedTimeSteppingAnalysisForModulation(_6805.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''DatumCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2126.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6701.DatumAdvancedTimeSteppingAnalysisForModulation]':
        '''List[DatumAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6701.DatumAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6701.DatumAdvancedTimeSteppingAnalysisForModulation]':
        '''List[DatumAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6701.DatumAdvancedTimeSteppingAnalysisForModulation))
        return value
