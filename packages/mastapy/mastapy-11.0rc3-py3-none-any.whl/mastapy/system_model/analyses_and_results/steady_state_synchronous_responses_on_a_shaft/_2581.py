﻿'''_2581.py

CVTPulleySteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2181
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2624
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'CVTPulleySteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleySteadyStateSynchronousResponseOnAShaft',)


class CVTPulleySteadyStateSynchronousResponseOnAShaft(_2624.PulleySteadyStateSynchronousResponseOnAShaft):
    '''CVTPulleySteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleySteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
