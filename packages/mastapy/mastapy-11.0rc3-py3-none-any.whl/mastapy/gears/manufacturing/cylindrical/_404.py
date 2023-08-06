﻿'''_404.py

CylindricalMeshManufacturingConfig
'''


from typing import List

from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _488, _489, _485
from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import _958
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalMeshManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshManufacturingConfig',)


class CylindricalMeshManufacturingConfig(_958.GearMeshImplementationDetail):
    '''CylindricalMeshManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MESH_MANUFACTURING_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalMeshManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def meshed_gear_a_as_manufactured(self) -> 'List[_488.CylindricalManufacturedRealGearInMesh]':
        '''List[CylindricalManufacturedRealGearInMesh]: 'MeshedGearAAsManufactured' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGearAAsManufactured, constructor.new(_488.CylindricalManufacturedRealGearInMesh))
        return value

    @property
    def meshed_gear_b_as_manufactured(self) -> 'List[_488.CylindricalManufacturedRealGearInMesh]':
        '''List[CylindricalManufacturedRealGearInMesh]: 'MeshedGearBAsManufactured' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGearBAsManufactured, constructor.new(_488.CylindricalManufacturedRealGearInMesh))
        return value

    @property
    def meshed_gear_a_as_manufactured_virtual(self) -> 'List[_489.CylindricalManufacturedVirtualGearInMesh]':
        '''List[CylindricalManufacturedVirtualGearInMesh]: 'MeshedGearAAsManufacturedVirtual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGearAAsManufacturedVirtual, constructor.new(_489.CylindricalManufacturedVirtualGearInMesh))
        return value

    @property
    def meshed_gear_b_as_manufactured_virtual(self) -> 'List[_489.CylindricalManufacturedVirtualGearInMesh]':
        '''List[CylindricalManufacturedVirtualGearInMesh]: 'MeshedGearBAsManufacturedVirtual' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGearBAsManufacturedVirtual, constructor.new(_489.CylindricalManufacturedVirtualGearInMesh))
        return value

    @property
    def gear_a_as_manufactured(self) -> 'List[_485.CutterSimulationCalc]':
        '''List[CutterSimulationCalc]: 'GearAAsManufactured' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearAAsManufactured, constructor.new(_485.CutterSimulationCalc))
        return value

    @property
    def gear_b_as_manufactured(self) -> 'List[_485.CutterSimulationCalc]':
        '''List[CutterSimulationCalc]: 'GearBAsManufactured' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearBAsManufactured, constructor.new(_485.CutterSimulationCalc))
        return value
