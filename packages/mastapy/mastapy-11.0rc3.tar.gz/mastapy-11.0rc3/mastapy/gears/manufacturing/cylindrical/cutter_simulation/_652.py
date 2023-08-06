﻿'''_652.py

CylindricalGearSpecification
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import (
    _1011, _972, _993, _1010
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CylindricalGearSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSpecification',)


class CylindricalGearSpecification(_0.APIBase):
    '''CylindricalGearSpecification

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def normal_module(self) -> 'float':
        '''float: 'NormalModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalModule

    @property
    def helix_angle(self) -> 'float':
        '''float: 'HelixAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixAngle

    @property
    def normal_pressure_angle(self) -> 'float':
        '''float: 'NormalPressureAngle' is the original name of this property.'''

        return self.wrapped.NormalPressureAngle

    @normal_pressure_angle.setter
    def normal_pressure_angle(self, value: 'float'):
        self.wrapped.NormalPressureAngle = float(value) if value else 0.0

    @property
    def number_of_teeth_unsigned(self) -> 'float':
        '''float: 'NumberOfTeethUnsigned' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfTeethUnsigned

    @property
    def tooth_thickness_specification(self) -> '_1011.ToothThicknessSpecificationBase':
        '''ToothThicknessSpecificationBase: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1011.ToothThicknessSpecificationBase.TYPE not in self.wrapped.ToothThicknessSpecification.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to ToothThicknessSpecificationBase. Expected: {}.'.format(self.wrapped.ToothThicknessSpecification.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThicknessSpecification.__class__)(self.wrapped.ToothThicknessSpecification) if self.wrapped.ToothThicknessSpecification else None

    @property
    def tooth_thickness_specification_of_type_finish_tooth_thickness_design_specification(self) -> '_972.FinishToothThicknessDesignSpecification':
        '''FinishToothThicknessDesignSpecification: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _972.FinishToothThicknessDesignSpecification.TYPE not in self.wrapped.ToothThicknessSpecification.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to FinishToothThicknessDesignSpecification. Expected: {}.'.format(self.wrapped.ToothThicknessSpecification.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThicknessSpecification.__class__)(self.wrapped.ToothThicknessSpecification) if self.wrapped.ToothThicknessSpecification else None

    @property
    def tooth_thickness_specification_of_type_readonly_tooth_thickness_specification(self) -> '_993.ReadonlyToothThicknessSpecification':
        '''ReadonlyToothThicknessSpecification: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _993.ReadonlyToothThicknessSpecification.TYPE not in self.wrapped.ToothThicknessSpecification.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to ReadonlyToothThicknessSpecification. Expected: {}.'.format(self.wrapped.ToothThicknessSpecification.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThicknessSpecification.__class__)(self.wrapped.ToothThicknessSpecification) if self.wrapped.ToothThicknessSpecification else None

    @property
    def tooth_thickness_specification_of_type_tooth_thickness_specification(self) -> '_1010.ToothThicknessSpecification':
        '''ToothThicknessSpecification: 'ToothThicknessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1010.ToothThicknessSpecification.TYPE not in self.wrapped.ToothThicknessSpecification.__class__.__mro__:
            raise CastException('Failed to cast tooth_thickness_specification to ToothThicknessSpecification. Expected: {}.'.format(self.wrapped.ToothThicknessSpecification.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ToothThicknessSpecification.__class__)(self.wrapped.ToothThicknessSpecification) if self.wrapped.ToothThicknessSpecification else None
