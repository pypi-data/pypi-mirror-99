﻿'''_4298.py

HypoidGearModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6543
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4239
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'HypoidGearModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearModalAnalysisAtAStiffness',)


class HypoidGearModalAnalysisAtAStiffness(_4239.AGMAGleasonConicalGearModalAnalysisAtAStiffness):
    '''HypoidGearModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2209.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6543.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6543.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
