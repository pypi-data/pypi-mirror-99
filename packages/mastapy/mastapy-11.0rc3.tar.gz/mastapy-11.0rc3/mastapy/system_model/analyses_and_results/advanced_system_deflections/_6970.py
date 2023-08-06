﻿'''_6970.py

FEPartAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6523
from mastapy.system_model.analyses_and_results.system_deflections import _2423
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6911
from mastapy._internal.python_net import python_net_import

_FE_PART_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FEPartAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartAdvancedSystemDeflection',)


class FEPartAdvancedSystemDeflection(_6911.AbstractShaftOrHousingAdvancedSystemDeflection):
    '''FEPartAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FE_PART_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartAdvancedSystemDeflection.TYPE'):
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
    def planetaries(self) -> 'List[FEPartAdvancedSystemDeflection]':
        '''List[FEPartAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartAdvancedSystemDeflection))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2423.FEPartSystemDeflection]':
        '''List[FEPartSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2423.FEPartSystemDeflection))
        return value
