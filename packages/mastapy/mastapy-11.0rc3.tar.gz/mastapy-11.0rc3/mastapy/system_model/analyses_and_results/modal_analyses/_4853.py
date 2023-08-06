﻿'''_4853.py

ShaftModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2158
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6588
from mastapy.system_model.analyses_and_results.system_deflections import _2470
from mastapy.system_model.analyses_and_results.modal_analyses import _4752
from mastapy._internal.python_net import python_net_import

_SHAFT_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ShaftModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftModalAnalysis',)


class ShaftModalAnalysis(_4752.AbstractShaftModalAnalysis):
    '''ShaftModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2158.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2158.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6588.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6588.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2470.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2470.ShaftSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[ShaftModalAnalysis]':
        '''List[ShaftModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftModalAnalysis))
        return value
