﻿'''_3218.py

DatumSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _2126
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6504
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3192
from mastapy._internal.python_net import python_net_import

_DATUM_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'DatumSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumSteadyStateSynchronousResponse',)


class DatumSteadyStateSynchronousResponse(_3192.ComponentSteadyStateSynchronousResponse):
    '''DatumSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _DATUM_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2126.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6504.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
