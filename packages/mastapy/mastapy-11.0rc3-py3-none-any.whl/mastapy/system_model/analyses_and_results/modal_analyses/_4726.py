﻿'''_4726.py

BearingModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2089
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6418
from mastapy.system_model.analyses_and_results.system_deflections import _2333
from mastapy.system_model.analyses_and_results.modal_analyses import _4754
from mastapy._internal.python_net import python_net_import

_BEARING_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BearingModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingModalAnalysis',)


class BearingModalAnalysis(_4754.ConnectorModalAnalysis):
    '''BearingModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2089.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6418.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6418.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2333.BearingSystemDeflection':
        '''BearingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2333.BearingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[BearingModalAnalysis]':
        '''List[BearingModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingModalAnalysis))
        return value
