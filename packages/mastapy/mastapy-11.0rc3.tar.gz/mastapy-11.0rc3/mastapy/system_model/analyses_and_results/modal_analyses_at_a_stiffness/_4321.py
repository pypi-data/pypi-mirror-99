﻿'''_4321.py

PointLoadModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _2148
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6576
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4357
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'PointLoadModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadModalAnalysisAtAStiffness',)


class PointLoadModalAnalysisAtAStiffness(_4357.VirtualComponentModalAnalysisAtAStiffness):
    '''PointLoadModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2148.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2148.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6576.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6576.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
