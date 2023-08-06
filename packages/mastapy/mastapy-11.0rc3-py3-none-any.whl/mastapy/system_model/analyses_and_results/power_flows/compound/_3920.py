﻿'''_3920.py

RollingRingAssemblyCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2272
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3790
from mastapy.system_model.analyses_and_results.power_flows.compound import _3927
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RollingRingAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyCompoundPowerFlow',)


class RollingRingAssemblyCompoundPowerFlow(_3927.SpecialisedAssemblyCompoundPowerFlow):
    '''RollingRingAssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyCompoundPowerFlow.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_3790.RollingRingAssemblyPowerFlow]':
        '''List[RollingRingAssemblyPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3790.RollingRingAssemblyPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3790.RollingRingAssemblyPowerFlow]':
        '''List[RollingRingAssemblyPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3790.RollingRingAssemblyPowerFlow))
        return value
