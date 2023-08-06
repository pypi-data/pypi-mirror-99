﻿'''_2140.py

PlanetaryGearSet
'''


from typing import List

from mastapy.system_model.part_model.gears import _2123, _2125, _2124
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSet',)


class PlanetaryGearSet(_2124.CylindricalGearSet):
    '''PlanetaryGearSet

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def suns(self) -> 'List[_2123.CylindricalGear]':
        '''List[CylindricalGear]: 'Suns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Suns, constructor.new(_2123.CylindricalGear))
        return value

    @property
    def planets(self) -> 'List[_2125.CylindricalPlanetGear]':
        '''List[CylindricalPlanetGear]: 'Planets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planets, constructor.new(_2125.CylindricalPlanetGear))
        return value

    @property
    def annuluses(self) -> 'List[_2123.CylindricalGear]':
        '''List[CylindricalGear]: 'Annuluses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Annuluses, constructor.new(_2123.CylindricalGear))
        return value

    def add_sun(self) -> '_2123.CylindricalGear':
        ''' 'AddSun' is the original name of this method.

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        '''

        method_result = self.wrapped.AddSun()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_planet(self) -> '_2123.CylindricalGear':
        ''' 'AddPlanet' is the original name of this method.

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        '''

        method_result = self.wrapped.AddPlanet()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def set_number_of_planets(self, amount: 'int'):
        ''' 'SetNumberOfPlanets' is the original name of this method.

        Args:
            amount (int)
        '''

        amount = int(amount)
        self.wrapped.SetNumberOfPlanets(amount if amount else 0)
