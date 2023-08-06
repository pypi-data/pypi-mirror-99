﻿'''_180.py

HypoidVirtualCylindricalGearISO10300MethodB2
'''


from mastapy._internal import constructor
from mastapy.gears.rating.virtual_cylindrical_gears import _190
from mastapy._internal.python_net import python_net_import

_HYPOID_VIRTUAL_CYLINDRICAL_GEAR_ISO10300_METHOD_B2 = python_net_import('SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears', 'HypoidVirtualCylindricalGearISO10300MethodB2')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidVirtualCylindricalGearISO10300MethodB2',)


class HypoidVirtualCylindricalGearISO10300MethodB2(_190.VirtualCylindricalGearISO10300MethodB2):
    '''HypoidVirtualCylindricalGearISO10300MethodB2

    This is a mastapy class.
    '''

    TYPE = _HYPOID_VIRTUAL_CYLINDRICAL_GEAR_ISO10300_METHOD_B2

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidVirtualCylindricalGearISO10300MethodB2.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
