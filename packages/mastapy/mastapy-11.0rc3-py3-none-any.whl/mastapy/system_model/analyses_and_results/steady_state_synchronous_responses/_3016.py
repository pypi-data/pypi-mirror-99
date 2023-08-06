﻿'''_3016.py

BearingSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2026
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6104
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3044
from mastapy._internal.python_net import python_net_import

_BEARING_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'BearingSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSteadyStateSynchronousResponse',)


class BearingSteadyStateSynchronousResponse(_3044.ConnectorSteadyStateSynchronousResponse):
    '''BearingSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BEARING_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2026.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2026.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6104.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6104.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[BearingSteadyStateSynchronousResponse]':
        '''List[BearingSteadyStateSynchronousResponse]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingSteadyStateSynchronousResponse))
        return value
