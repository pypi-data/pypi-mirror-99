﻿'''_6067.py

ClutchCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5938
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6083
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ClutchCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundDynamicAnalysis',)


class ClutchCompoundDynamicAnalysis(_6083.CouplingCompoundDynamicAnalysis):
    '''ClutchCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2253.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2253.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5938.ClutchDynamicAnalysis]':
        '''List[ClutchDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5938.ClutchDynamicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5938.ClutchDynamicAnalysis]':
        '''List[ClutchDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5938.ClutchDynamicAnalysis))
        return value
