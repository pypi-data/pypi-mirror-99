﻿'''_2536.py

BoltCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2378
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2542
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BoltCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundSystemDeflection',)


class BoltCompoundSystemDeflection(_2542.ComponentCompoundSystemDeflection):
    '''BoltCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2378.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2378.BoltSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2378.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2378.BoltSystemDeflection))
        return value
