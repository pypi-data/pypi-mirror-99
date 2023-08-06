﻿'''_6075.py

ConceptGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5945
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6104
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ConceptGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundDynamicAnalysis',)


class ConceptGearCompoundDynamicAnalysis(_6104.GearCompoundDynamicAnalysis):
    '''ConceptGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5945.ConceptGearDynamicAnalysis]':
        '''List[ConceptGearDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5945.ConceptGearDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5945.ConceptGearDynamicAnalysis]':
        '''List[ConceptGearDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5945.ConceptGearDynamicAnalysis))
        return value
