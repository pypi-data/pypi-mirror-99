﻿'''_3330.py

ConceptGearMeshCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3196
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3359
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ConceptGearMeshCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshCompoundSteadyStateSynchronousResponse',)


class ConceptGearMeshCompoundSteadyStateSynchronousResponse(_3359.GearMeshCompoundSteadyStateSynchronousResponse):
    '''ConceptGearMeshCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1985.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1985.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3196.ConceptGearMeshSteadyStateSynchronousResponse]':
        '''List[ConceptGearMeshSteadyStateSynchronousResponse]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3196.ConceptGearMeshSteadyStateSynchronousResponse))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3196.ConceptGearMeshSteadyStateSynchronousResponse]':
        '''List[ConceptGearMeshSteadyStateSynchronousResponse]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3196.ConceptGearMeshSteadyStateSynchronousResponse))
        return value
