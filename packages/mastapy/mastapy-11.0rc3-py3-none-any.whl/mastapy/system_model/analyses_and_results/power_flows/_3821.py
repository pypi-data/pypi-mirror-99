﻿'''_3821.py

UnbalancedMassPowerFlow
'''


from mastapy.system_model.part_model import _2154
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6621
from mastapy.system_model.analyses_and_results.power_flows import _3822
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'UnbalancedMassPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassPowerFlow',)


class UnbalancedMassPowerFlow(_3822.VirtualComponentPowerFlow):
    '''UnbalancedMassPowerFlow

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2154.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6621.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6621.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
