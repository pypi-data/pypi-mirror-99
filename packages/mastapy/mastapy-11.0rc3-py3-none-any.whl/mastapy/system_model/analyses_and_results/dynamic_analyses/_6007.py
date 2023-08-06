﻿'''_6007.py

RingPinsToDiscConnectionDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2021
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6582
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5982
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RingPinsToDiscConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionDynamicAnalysis',)


class RingPinsToDiscConnectionDynamicAnalysis(_5982.InterMountableComponentConnectionDynamicAnalysis):
    '''RingPinsToDiscConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2021.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6582.RingPinsToDiscConnectionLoadCase':
        '''RingPinsToDiscConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6582.RingPinsToDiscConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
