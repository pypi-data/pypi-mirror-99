﻿'''_3917.py

PulleyCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2265, _2262
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows import _3787
from mastapy.system_model.analyses_and_results.power_flows.compound import _3868
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PulleyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundPowerFlow',)


class PulleyCompoundPowerFlow(_3868.CouplingHalfCompoundPowerFlow):
    '''PulleyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2265.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2265.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3787.PulleyPowerFlow]':
        '''List[PulleyPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3787.PulleyPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3787.PulleyPowerFlow]':
        '''List[PulleyPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3787.PulleyPowerFlow))
        return value
