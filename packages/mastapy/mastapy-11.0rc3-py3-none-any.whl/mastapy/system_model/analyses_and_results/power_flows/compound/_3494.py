﻿'''_3494.py

ShaftToMountableComponentConnectionCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3438
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ShaftToMountableComponentConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftToMountableComponentConnectionCompoundPowerFlow',)


class ShaftToMountableComponentConnectionCompoundPowerFlow(_3438.ConnectionCompoundPowerFlow):
    '''ShaftToMountableComponentConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftToMountableComponentConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
