﻿'''_3566.py

CVTPulleyParametricStudyTool
'''


from mastapy.system_model.part_model.couplings import _2181
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3626
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CVTPulleyParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyParametricStudyTool',)


class CVTPulleyParametricStudyTool(_3626.PulleyParametricStudyTool):
    '''CVTPulleyParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
