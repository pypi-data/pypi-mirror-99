﻿'''_4393.py

UnbalancedMassModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _2077
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6277
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4394
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'UnbalancedMassModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassModalAnalysisAtAStiffness',)


class UnbalancedMassModalAnalysisAtAStiffness(_4394.VirtualComponentModalAnalysisAtAStiffness):
    '''UnbalancedMassModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2077.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2077.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6277.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6277.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
