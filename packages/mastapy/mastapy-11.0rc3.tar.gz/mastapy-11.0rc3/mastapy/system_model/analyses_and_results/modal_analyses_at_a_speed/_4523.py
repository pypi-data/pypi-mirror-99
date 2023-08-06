﻿'''_4523.py

ConceptGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2196
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6476
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4552
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ConceptGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearModalAnalysisAtASpeed',)


class ConceptGearModalAnalysisAtASpeed(_4552.GearModalAnalysisAtASpeed):
    '''ConceptGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearModalAnalysisAtASpeed.TYPE'):
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
    def component_load_case(self) -> '_6476.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6476.ConceptGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
