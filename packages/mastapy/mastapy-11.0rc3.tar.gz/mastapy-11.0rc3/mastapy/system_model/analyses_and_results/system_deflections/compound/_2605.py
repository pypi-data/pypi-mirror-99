﻿'''_2605.py

PowerLoadCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2149
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2458
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2641
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PowerLoadCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundSystemDeflection',)


class PowerLoadCompoundSystemDeflection(_2641.VirtualComponentCompoundSystemDeflection):
    '''PowerLoadCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2149.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2458.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2458.PowerLoadSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2458.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2458.PowerLoadSystemDeflection))
        return value
