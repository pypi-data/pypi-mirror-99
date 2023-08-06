﻿'''_634.py

ProcessSimulationViewModel
'''


from typing import Generic, TypeVar

from mastapy.gears.manufacturing.cylindrical import _575
from mastapy._internal.python_net import python_net_import

_PROCESS_SIMULATION_VIEW_MODEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessSimulationViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessSimulationViewModel',)


T = TypeVar('T')


class ProcessSimulationViewModel(_575.GearManufacturingConfigurationViewModel, Generic[T]):
    '''ProcessSimulationViewModel

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _PROCESS_SIMULATION_VIEW_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessSimulationViewModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
