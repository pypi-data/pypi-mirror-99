﻿'''_3419.py

BevelGearCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3407
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BevelGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearCompoundPowerFlow',)


class BevelGearCompoundPowerFlow(_3407.AGMAGleasonConicalGearCompoundPowerFlow):
    '''BevelGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
