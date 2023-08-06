﻿'''_2917.py

BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1918
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2794
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _2922
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed',)


class BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed(_2922.BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed):
    '''BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1918.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1918.BevelDifferentialGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1918.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1918.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2794.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2794.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def connection_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2794.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed]: 'ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2794.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
