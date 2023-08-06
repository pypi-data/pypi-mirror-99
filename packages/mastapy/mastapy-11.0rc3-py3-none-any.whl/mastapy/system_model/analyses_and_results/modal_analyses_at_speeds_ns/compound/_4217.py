﻿'''_4217.py

KlingelnbergCycloPalloidConicalGearCompoundModalAnalysesAtSpeeds
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4187
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'KlingelnbergCycloPalloidConicalGearCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearCompoundModalAnalysesAtSpeeds',)


class KlingelnbergCycloPalloidConicalGearCompoundModalAnalysesAtSpeeds(_4187.ConicalGearCompoundModalAnalysesAtSpeeds):
    '''KlingelnbergCycloPalloidConicalGearCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
