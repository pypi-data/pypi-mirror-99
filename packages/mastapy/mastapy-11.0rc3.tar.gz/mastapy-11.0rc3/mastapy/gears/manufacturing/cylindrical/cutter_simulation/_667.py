﻿'''_667.py

WormGrinderSimulationCalculator
'''


from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _693
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _662
from mastapy._internal.python_net import python_net_import

_WORM_GRINDER_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'WormGrinderSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGrinderSimulationCalculator',)


class WormGrinderSimulationCalculator(_662.RackSimulationCalculator):
    '''WormGrinderSimulationCalculator

    This is a mastapy class.
    '''

    TYPE = _WORM_GRINDER_SIMULATION_CALCULATOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGrinderSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def worm_grinder(self) -> '_693.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'WormGrinder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_693.CylindricalGearWormGrinderShape)(self.wrapped.WormGrinder) if self.wrapped.WormGrinder else None
