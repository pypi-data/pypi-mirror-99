﻿'''_2773.py

WormGearMeshSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.connections_and_sockets.gears import _2009
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6624
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2707
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'WormGearMeshSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshSteadyStateSynchronousResponseOnAShaft',)


class WormGearMeshSteadyStateSynchronousResponseOnAShaft(_2707.GearMeshSteadyStateSynchronousResponseOnAShaft):
    '''WormGearMeshSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2009.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6624.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6624.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
