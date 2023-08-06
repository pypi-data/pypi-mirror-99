﻿'''_3381.py

PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3248
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3338
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse',)


class PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse(_3338.CouplingConnectionCompoundSteadyStateSynchronousResponse):
    '''PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2028.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.PartToPartShearCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2028.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3248.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingConnectionSteadyStateSynchronousResponse]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3248.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3248.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingConnectionSteadyStateSynchronousResponse]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3248.PartToPartShearCouplingConnectionSteadyStateSynchronousResponse))
        return value
