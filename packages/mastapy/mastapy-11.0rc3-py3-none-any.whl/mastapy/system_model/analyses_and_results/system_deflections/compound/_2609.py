﻿'''_2609.py

RollingRingAssemblyCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2272
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2463
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2617
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'RollingRingAssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyCompoundSystemDeflection',)


class RollingRingAssemblyCompoundSystemDeflection(_2617.SpecialisedAssemblyCompoundSystemDeflection):
    '''RollingRingAssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2272.RollingRingAssembly':
        '''RollingRingAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.RollingRingAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2272.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2463.RollingRingAssemblySystemDeflection]':
        '''List[RollingRingAssemblySystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2463.RollingRingAssemblySystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2463.RollingRingAssemblySystemDeflection]':
        '''List[RollingRingAssemblySystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2463.RollingRingAssemblySystemDeflection))
        return value
