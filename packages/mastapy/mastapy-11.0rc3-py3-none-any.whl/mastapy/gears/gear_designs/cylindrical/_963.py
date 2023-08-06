﻿'''_963.py

CylindricalMeshAngularBacklash
'''


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _966
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_ANGULAR_BACKLASH = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalMeshAngularBacklash')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshAngularBacklash',)


class CylindricalMeshAngularBacklash(_966.CylindricalMeshLinearBacklashSpecification):
    '''CylindricalMeshAngularBacklash

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MESH_ANGULAR_BACKLASH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalMeshAngularBacklash.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Minimum' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Minimum) if self.wrapped.Minimum else None

    @minimum.setter
    def minimum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Minimum = value

    @property
    def maximum(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Maximum' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Maximum) if self.wrapped.Maximum else None

    @maximum.setter
    def maximum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Maximum = value

    @property
    def average_mean(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AverageMean' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AverageMean) if self.wrapped.AverageMean else None

    @average_mean.setter
    def average_mean(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AverageMean = value

    @property
    def spread(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Spread' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Spread) if self.wrapped.Spread else None

    @spread.setter
    def spread(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Spread = value
