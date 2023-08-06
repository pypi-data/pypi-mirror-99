﻿'''_2756.py

BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2077
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6088
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2757, _2755, _2761
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed',)


class BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed(_2761.BevelGearSetSteadyStateSynchronousResponseAtASpeed):
    '''BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2077.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2077.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6088.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6088.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2757.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_2757.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bevel_differential_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2755.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_2755.BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
