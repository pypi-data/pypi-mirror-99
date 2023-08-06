﻿'''_3320.py

CVTPulleyPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2181
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3365
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CVTPulleyPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyPowerFlow',)


class CVTPulleyPowerFlow(_3365.PulleyPowerFlow):
    '''CVTPulleyPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
