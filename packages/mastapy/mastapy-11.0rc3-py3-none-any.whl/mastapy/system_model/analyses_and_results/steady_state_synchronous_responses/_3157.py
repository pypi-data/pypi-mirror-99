﻿'''_3157.py

ClutchSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2224
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6433
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3173
from mastapy._internal.python_net import python_net_import

_CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ClutchSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchSteadyStateSynchronousResponse',)


class ClutchSteadyStateSynchronousResponse(_3173.CouplingSteadyStateSynchronousResponse):
    '''ClutchSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2224.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6433.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6433.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
