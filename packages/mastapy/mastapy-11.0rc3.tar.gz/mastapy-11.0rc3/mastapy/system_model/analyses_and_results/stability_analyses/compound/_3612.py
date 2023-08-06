﻿'''_3612.py

DatumCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3481
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3586
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'DatumCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundStabilityAnalysis',)


class DatumCompoundStabilityAnalysis(_3586.ComponentCompoundStabilityAnalysis):
    '''DatumCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundStabilityAnalysis.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_3481.DatumStabilityAnalysis]':
        '''List[DatumStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3481.DatumStabilityAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3481.DatumStabilityAnalysis]':
        '''List[DatumStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3481.DatumStabilityAnalysis))
        return value
