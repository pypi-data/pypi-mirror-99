﻿'''_4166.py

GuideDxfModelCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2132
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4026
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4130
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GuideDxfModelCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundParametricStudyTool',)


class GuideDxfModelCompoundParametricStudyTool(_4130.ComponentCompoundParametricStudyTool):
    '''GuideDxfModelCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2132.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4026.GuideDxfModelParametricStudyTool]':
        '''List[GuideDxfModelParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4026.GuideDxfModelParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4026.GuideDxfModelParametricStudyTool]':
        '''List[GuideDxfModelParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4026.GuideDxfModelParametricStudyTool))
        return value
