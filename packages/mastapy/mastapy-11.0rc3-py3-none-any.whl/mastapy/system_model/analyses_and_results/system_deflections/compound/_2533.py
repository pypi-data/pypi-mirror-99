﻿'''_2533.py

BevelGearCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2376
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2521
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BevelGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearCompoundSystemDeflection',)


class BevelGearCompoundSystemDeflection(_2521.AGMAGleasonConicalGearCompoundSystemDeflection):
    '''BevelGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_2376.BevelGearSystemDeflection]':
        '''List[BevelGearSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2376.BevelGearSystemDeflection))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_2376.BevelGearSystemDeflection]':
        '''List[BevelGearSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2376.BevelGearSystemDeflection))
        return value
