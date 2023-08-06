﻿'''_1963.py

CylindricalGearMesh
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2172, _2188, _2171
from mastapy._internal.cast_exception import CastException
from mastapy.math_utility.measured_ranges import _1564
from mastapy.gears.gear_designs.cylindrical import _948
from mastapy.system_model.connections_and_sockets.gears import _1967
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMesh',)


class CylindricalGearMesh(_1967.GearMesh):
    '''CylindricalGearMesh

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance_with_normal_module_adjustment_by_scaling_entire_model(self) -> 'float':
        '''float: 'CentreDistanceWithNormalModuleAdjustmentByScalingEntireModel' is the original name of this property.'''

        return self.wrapped.CentreDistanceWithNormalModuleAdjustmentByScalingEntireModel

    @centre_distance_with_normal_module_adjustment_by_scaling_entire_model.setter
    def centre_distance_with_normal_module_adjustment_by_scaling_entire_model(self, value: 'float'):
        self.wrapped.CentreDistanceWithNormalModuleAdjustmentByScalingEntireModel = float(value) if value else 0.0

    @property
    def is_centre_distance_ready_to_change(self) -> 'bool':
        '''bool: 'IsCentreDistanceReadyToChange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsCentreDistanceReadyToChange

    @property
    def cylindrical_gear_set(self) -> '_2172.CylindricalGearSet':
        '''CylindricalGearSet: 'CylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.CylindricalGearSet.TYPE not in self.wrapped.CylindricalGearSet.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_set to CylindricalGearSet. Expected: {}.'.format(self.wrapped.CylindricalGearSet.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSet.__class__)(self.wrapped.CylindricalGearSet) if self.wrapped.CylindricalGearSet else None

    @property
    def centre_distance_range(self) -> '_1564.ShortLengthRange':
        '''ShortLengthRange: 'CentreDistanceRange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1564.ShortLengthRange)(self.wrapped.CentreDistanceRange) if self.wrapped.CentreDistanceRange else None

    @property
    def cylindrical_gear_mesh_design(self) -> '_948.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'CylindricalGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_948.CylindricalGearMeshDesign)(self.wrapped.CylindricalGearMeshDesign) if self.wrapped.CylindricalGearMeshDesign else None

    @property
    def cylindrical_gears(self) -> 'List[_2171.CylindricalGear]':
        '''List[CylindricalGear]: 'CylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGears, constructor.new(_2171.CylindricalGear))
        return value
