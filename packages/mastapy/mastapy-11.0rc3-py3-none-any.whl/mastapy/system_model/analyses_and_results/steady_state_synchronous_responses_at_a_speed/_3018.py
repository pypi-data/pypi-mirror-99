﻿'''_3018.py

StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2223
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6604
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3019, _3017, _2925
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed',)


class StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed(_2925.BevelGearSetSteadyStateSynchronousResponseAtASpeed):
    '''StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2223.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6604.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6604.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3019.StraightBevelGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_3019.StraightBevelGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3017.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_3017.StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
