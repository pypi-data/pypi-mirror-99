﻿'''_2613.py

ShaftCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2158
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2614, _2518
from mastapy.system_model.analyses_and_results.system_deflections import _2470
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ShaftCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundSystemDeflection',)


class ShaftCompoundSystemDeflection(_2518.AbstractShaftCompoundSystemDeflection):
    '''ShaftCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundSystemDeflection.TYPE'):
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
    def shaft_duty_cycle_damage_results(self) -> '_2614.ShaftDutyCycleSystemDeflection':
        '''ShaftDutyCycleSystemDeflection: 'ShaftDutyCycleDamageResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2614.ShaftDutyCycleSystemDeflection)(self.wrapped.ShaftDutyCycleDamageResults) if self.wrapped.ShaftDutyCycleDamageResults else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2470.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2470.ShaftSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundSystemDeflection]':
        '''List[ShaftCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2470.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2470.ShaftSystemDeflection))
        return value
