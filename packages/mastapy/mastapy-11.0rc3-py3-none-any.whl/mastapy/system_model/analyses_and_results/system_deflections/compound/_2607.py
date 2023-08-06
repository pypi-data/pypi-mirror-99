﻿'''_2607.py

RingPinsCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2245
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2460
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2595
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'RingPinsCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundSystemDeflection',)


class RingPinsCompoundSystemDeflection(_2595.MountableComponentCompoundSystemDeflection):
    '''RingPinsCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2245.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2245.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2460.RingPinsSystemDeflection]':
        '''List[RingPinsSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_2460.RingPinsSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2460.RingPinsSystemDeflection]':
        '''List[RingPinsSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_2460.RingPinsSystemDeflection))
        return value
