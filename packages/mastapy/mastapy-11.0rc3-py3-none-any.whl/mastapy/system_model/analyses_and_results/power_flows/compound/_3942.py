﻿'''_3942.py

SynchroniserCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2277
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3814
from mastapy.system_model.analyses_and_results.power_flows.compound import _3927
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SynchroniserCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundPowerFlow',)


class SynchroniserCompoundPowerFlow(_3927.SpecialisedAssemblyCompoundPowerFlow):
    '''SynchroniserCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2277.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2277.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_3814.SynchroniserPowerFlow]':
        '''List[SynchroniserPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_3814.SynchroniserPowerFlow))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3814.SynchroniserPowerFlow]':
        '''List[SynchroniserPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_3814.SynchroniserPowerFlow))
        return value
