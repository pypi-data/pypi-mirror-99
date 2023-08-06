﻿'''_2608.py

RingPinsToDiscConnectionCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2021
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2461
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2583
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'RingPinsToDiscConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundSystemDeflection',)


class RingPinsToDiscConnectionCompoundSystemDeflection(_2583.InterMountableComponentConnectionCompoundSystemDeflection):
    '''RingPinsToDiscConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2021.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.RingPinsToDiscConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2021.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_2461.RingPinsToDiscConnectionSystemDeflection]':
        '''List[RingPinsToDiscConnectionSystemDeflection]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_2461.RingPinsToDiscConnectionSystemDeflection))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_2461.RingPinsToDiscConnectionSystemDeflection]':
        '''List[RingPinsToDiscConnectionSystemDeflection]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_2461.RingPinsToDiscConnectionSystemDeflection))
        return value
