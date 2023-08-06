﻿'''_1504.py

ModalCMSResults
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.nodal_analysis.component_mode_synthesis import _1505
from mastapy._internal.python_net import python_net_import

_MODAL_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'ModalCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalCMSResults',)


class ModalCMSResults(_1505.RealCMSResults):
    '''ModalCMSResults

    This is a mastapy class.
    '''

    TYPE = _MODAL_CMS_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculate_strain_and_kinetic_energy(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateStrainAndKineticEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateStrainAndKineticEnergy

    @property
    def calculate_results(self) -> 'bool':
        '''bool: 'CalculateResults' is the original name of this property.'''

        return self.wrapped.CalculateResults

    @calculate_results.setter
    def calculate_results(self, value: 'bool'):
        self.wrapped.CalculateResults = bool(value) if value else False
