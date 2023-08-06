﻿'''_7047.py

AbstractShaftOrHousingCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6911
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7070
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'AbstractShaftOrHousingCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingCompoundAdvancedSystemDeflection',)


class AbstractShaftOrHousingCompoundAdvancedSystemDeflection(_7070.ComponentCompoundAdvancedSystemDeflection):
    '''AbstractShaftOrHousingCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_6911.AbstractShaftOrHousingAdvancedSystemDeflection]':
        '''List[AbstractShaftOrHousingAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6911.AbstractShaftOrHousingAdvancedSystemDeflection))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_6911.AbstractShaftOrHousingAdvancedSystemDeflection]':
        '''List[AbstractShaftOrHousingAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6911.AbstractShaftOrHousingAdvancedSystemDeflection))
        return value
