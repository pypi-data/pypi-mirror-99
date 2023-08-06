﻿'''_5973.py

FEPartDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6523
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5918
from mastapy._internal.python_net import python_net_import

_FE_PART_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'FEPartDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartDynamicAnalysis',)


class FEPartDynamicAnalysis(_5918.AbstractShaftOrHousingDynamicAnalysis):
    '''FEPartDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2130.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6523.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6523.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[FEPartDynamicAnalysis]':
        '''List[FEPartDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartDynamicAnalysis))
        return value
