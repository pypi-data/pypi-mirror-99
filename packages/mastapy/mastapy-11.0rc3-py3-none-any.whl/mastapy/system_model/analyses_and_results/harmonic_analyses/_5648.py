﻿'''_5648.py

ElectricMachineRotorXForcePeriodicExcitationDetail
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses import _5647
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_ROTOR_X_FORCE_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ElectricMachineRotorXForcePeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineRotorXForcePeriodicExcitationDetail',)


class ElectricMachineRotorXForcePeriodicExcitationDetail(_5647.ElectricMachinePeriodicExcitationDetail):
    '''ElectricMachineRotorXForcePeriodicExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_ROTOR_X_FORCE_PERIODIC_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineRotorXForcePeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
