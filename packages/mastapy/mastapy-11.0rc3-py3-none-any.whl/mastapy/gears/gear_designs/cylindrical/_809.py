﻿'''_809.py

ISO6336Geometry
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _810
from mastapy._internal.python_net import python_net_import

_ISO6336_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ISO6336Geometry')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336Geometry',)


class ISO6336Geometry(_810.ISO6336GeometryBase):
    '''ISO6336Geometry

    This is a mastapy class.
    '''

    TYPE = _ISO6336_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO6336Geometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso6336_tooth_root_chord(self) -> 'float':
        '''float: 'ISO6336ToothRootChord' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO6336ToothRootChord

    @property
    def iso6336_root_fillet_radius(self) -> 'float':
        '''float: 'ISO6336RootFilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO6336RootFilletRadius
