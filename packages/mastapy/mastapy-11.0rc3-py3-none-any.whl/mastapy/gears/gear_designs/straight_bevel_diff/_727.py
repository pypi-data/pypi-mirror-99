﻿'''_727.py

StraightBevelDiffGearMeshDesign
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.straight_bevel_diff import _728, _726, _729
from mastapy.gears.gear_designs.bevel import _917
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.StraightBevelDiff', 'StraightBevelDiffGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshDesign',)


class StraightBevelDiffGearMeshDesign(_917.BevelGearMeshDesign):
    '''StraightBevelDiffGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pinion_performance_torque(self) -> 'float':
        '''float: 'PinionPerformanceTorque' is the original name of this property.'''

        return self.wrapped.PinionPerformanceTorque

    @pinion_performance_torque.setter
    def pinion_performance_torque(self, value: 'float'):
        self.wrapped.PinionPerformanceTorque = float(value) if value else 0.0

    @property
    def straight_bevel_diff_gear_set(self) -> '_728.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'StraightBevelDiffGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_728.StraightBevelDiffGearSetDesign)(self.wrapped.StraightBevelDiffGearSet) if self.wrapped.StraightBevelDiffGearSet else None

    @property
    def straight_bevel_diff_gears(self) -> 'List[_726.StraightBevelDiffGearDesign]':
        '''List[StraightBevelDiffGearDesign]: 'StraightBevelDiffGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGears, constructor.new(_726.StraightBevelDiffGearDesign))
        return value

    @property
    def straight_bevel_diff_meshed_gears(self) -> 'List[_729.StraightBevelDiffMeshedGearDesign]':
        '''List[StraightBevelDiffMeshedGearDesign]: 'StraightBevelDiffMeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshedGears, constructor.new(_729.StraightBevelDiffMeshedGearDesign))
        return value
