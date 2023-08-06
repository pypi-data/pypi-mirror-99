﻿'''_2513.py

BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2077
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6088
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2514, _2512, _2518
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft',)


class BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft(_2518.BevelGearSetSteadyStateSynchronousResponseOnAShaft):
    '''BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft.TYPE'):
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
    def bevel_differential_gears_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2514.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft]: 'BevelDifferentialGearsSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsSteadyStateSynchronousResponseOnAShaft, constructor.new(_2514.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bevel_differential_meshes_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2512.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft]: 'BevelDifferentialMeshesSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesSteadyStateSynchronousResponseOnAShaft, constructor.new(_2512.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value
