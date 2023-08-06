﻿'''_2832.py

FaceGearMeshSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.connections_and_sockets.gears import _1928
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6184
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2836
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'FaceGearMeshSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshSteadyStateSynchronousResponseAtASpeed',)


class FaceGearMeshSteadyStateSynchronousResponseAtASpeed(_2836.GearMeshSteadyStateSynchronousResponseAtASpeed):
    '''FaceGearMeshSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1928.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1928.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6184.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6184.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
