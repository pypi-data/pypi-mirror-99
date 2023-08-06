﻿'''_3084.py

HypoidGearMeshSteadyStateSynchronousResponse
'''


from mastapy.system_model.connections_and_sockets.gears import _1932
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6204
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3030
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'HypoidGearMeshSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshSteadyStateSynchronousResponse',)


class HypoidGearMeshSteadyStateSynchronousResponse(_3030.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse):
    '''HypoidGearMeshSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1932.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6204.HypoidGearMeshLoadCase':
        '''HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6204.HypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
