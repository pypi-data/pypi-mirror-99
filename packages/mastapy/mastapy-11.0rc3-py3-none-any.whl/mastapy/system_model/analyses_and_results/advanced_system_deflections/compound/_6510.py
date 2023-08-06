﻿'''_6510.py

PointLoadCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2071
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6388
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6544
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'PointLoadCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundAdvancedSystemDeflection',)


class PointLoadCompoundAdvancedSystemDeflection(_6544.VirtualComponentCompoundAdvancedSystemDeflection):
    '''PointLoadCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2071.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2071.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6388.PointLoadAdvancedSystemDeflection]':
        '''List[PointLoadAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6388.PointLoadAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6388.PointLoadAdvancedSystemDeflection]':
        '''List[PointLoadAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6388.PointLoadAdvancedSystemDeflection))
        return value
