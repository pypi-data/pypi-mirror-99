﻿'''_2956.py

CylindricalGearSetSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2201, _2217
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6500, _6571
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2957, _2955, _2967
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'CylindricalGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetSteadyStateSynchronousResponseAtASpeed',)


class CylindricalGearSetSteadyStateSynchronousResponseAtASpeed(_2967.GearSetSteadyStateSynchronousResponseAtASpeed):
    '''CylindricalGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2201.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2201.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6500.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6500.CylindricalGearSetLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2957.CylindricalGearSteadyStateSynchronousResponseAtASpeed]':
        '''List[CylindricalGearSteadyStateSynchronousResponseAtASpeed]: 'CylindricalGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsSteadyStateSynchronousResponseAtASpeed, constructor.new(_2957.CylindricalGearSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cylindrical_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_2955.CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed]':
        '''List[CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed]: 'CylindricalMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesSteadyStateSynchronousResponseAtASpeed, constructor.new(_2955.CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed))
        return value
