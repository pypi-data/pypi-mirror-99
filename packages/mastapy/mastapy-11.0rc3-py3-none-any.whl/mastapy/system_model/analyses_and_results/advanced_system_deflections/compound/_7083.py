﻿'''_7083.py

CouplingConnectionCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6951
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7110
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'CouplingConnectionCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundAdvancedSystemDeflection',)


class CouplingConnectionCompoundAdvancedSystemDeflection(_7110.InterMountableComponentConnectionCompoundAdvancedSystemDeflection):
    '''CouplingConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_6951.CouplingConnectionAdvancedSystemDeflection]':
        '''List[CouplingConnectionAdvancedSystemDeflection]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_6951.CouplingConnectionAdvancedSystemDeflection))
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_6951.CouplingConnectionAdvancedSystemDeflection]':
        '''List[CouplingConnectionAdvancedSystemDeflection]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_6951.CouplingConnectionAdvancedSystemDeflection))
        return value
