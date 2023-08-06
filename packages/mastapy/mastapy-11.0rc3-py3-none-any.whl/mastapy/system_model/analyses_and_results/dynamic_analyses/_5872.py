﻿'''_5872.py

BeltConnectionDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1888, _1893
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6125, _6158
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5926
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'BeltConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionDynamicAnalysis',)


class BeltConnectionDynamicAnalysis(_5926.InterMountableComponentConnectionDynamicAnalysis):
    '''BeltConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1888.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1888.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6125.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6125.BeltConnectionLoadCase.TYPE not in self.wrapped.ConnectionLoadCase.__class__.__mro__:
            raise CastException('Failed to cast connection_load_case to BeltConnectionLoadCase. Expected: {}.'.format(self.wrapped.ConnectionLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionLoadCase.__class__)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
