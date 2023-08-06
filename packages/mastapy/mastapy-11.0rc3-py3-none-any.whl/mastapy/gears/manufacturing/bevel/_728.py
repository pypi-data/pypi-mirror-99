﻿'''_728.py

ConicalMeshFlankManufacturingConfig
'''


from mastapy.gears.manufacturing.bevel.control_parameters import (
    _764, _765, _766, _767
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _770, _771
from mastapy.gears.manufacturing.bevel import _729
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_FLANK_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshFlankManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshFlankManufacturingConfig',)


class ConicalMeshFlankManufacturingConfig(_729.ConicalMeshFlankMicroGeometryConfig):
    '''ConicalMeshFlankManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_FLANK_MANUFACTURING_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshFlankManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def control_parameters(self) -> '_764.ConicalGearManufacturingControlParameters':
        '''ConicalGearManufacturingControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _764.ConicalGearManufacturingControlParameters.TYPE not in self.wrapped.ControlParameters.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalGearManufacturingControlParameters. Expected: {}.'.format(self.wrapped.ControlParameters.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ControlParameters.__class__)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def control_parameters_of_type_conical_manufacturing_sgm_control_parameters(self) -> '_765.ConicalManufacturingSGMControlParameters':
        '''ConicalManufacturingSGMControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _765.ConicalManufacturingSGMControlParameters.TYPE not in self.wrapped.ControlParameters.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSGMControlParameters. Expected: {}.'.format(self.wrapped.ControlParameters.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ControlParameters.__class__)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def control_parameters_of_type_conical_manufacturing_sgt_control_parameters(self) -> '_766.ConicalManufacturingSGTControlParameters':
        '''ConicalManufacturingSGTControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _766.ConicalManufacturingSGTControlParameters.TYPE not in self.wrapped.ControlParameters.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSGTControlParameters. Expected: {}.'.format(self.wrapped.ControlParameters.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ControlParameters.__class__)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def control_parameters_of_type_conical_manufacturing_smt_control_parameters(self) -> '_767.ConicalManufacturingSMTControlParameters':
        '''ConicalManufacturingSMTControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _767.ConicalManufacturingSMTControlParameters.TYPE not in self.wrapped.ControlParameters.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSMTControlParameters. Expected: {}.'.format(self.wrapped.ControlParameters.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ControlParameters.__class__)(self.wrapped.ControlParameters) if self.wrapped.ControlParameters else None

    @property
    def specified_phoenix_style_machine_settings(self) -> '_770.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'SpecifiedPhoenixStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_770.BasicConicalGearMachineSettingsGenerated)(self.wrapped.SpecifiedPhoenixStyleMachineSettings) if self.wrapped.SpecifiedPhoenixStyleMachineSettings else None

    @property
    def specified_cradle_style_machine_settings(self) -> '_771.CradleStyleConicalMachineSettingsGenerated':
        '''CradleStyleConicalMachineSettingsGenerated: 'SpecifiedCradleStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_771.CradleStyleConicalMachineSettingsGenerated)(self.wrapped.SpecifiedCradleStyleMachineSettings) if self.wrapped.SpecifiedCradleStyleMachineSettings else None
