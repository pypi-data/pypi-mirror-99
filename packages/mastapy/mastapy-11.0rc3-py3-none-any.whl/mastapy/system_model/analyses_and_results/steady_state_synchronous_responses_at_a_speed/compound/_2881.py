﻿'''_2881.py

BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _2877
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed(_2877.BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed):
    '''BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
