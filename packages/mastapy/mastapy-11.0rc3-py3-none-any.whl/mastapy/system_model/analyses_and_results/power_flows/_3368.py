﻿'''_3368.py

RollingRingPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2190
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6241
from mastapy.system_model.analyses_and_results.power_flows import _3316
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RollingRingPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingPowerFlow',)


class RollingRingPowerFlow(_3316.CouplingHalfPowerFlow):
    '''RollingRingPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2190.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6241.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6241.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
