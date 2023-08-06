﻿'''_178.py

BevelVirtualCylindricalGearSetISO10300MethodB1
'''


from mastapy.gears.rating.virtual_cylindrical_gears import _192
from mastapy._internal.python_net import python_net_import

_BEVEL_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B1 = python_net_import('SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears', 'BevelVirtualCylindricalGearSetISO10300MethodB1')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelVirtualCylindricalGearSetISO10300MethodB1',)


class BevelVirtualCylindricalGearSetISO10300MethodB1(_192.VirtualCylindricalGearSetISO10300MethodB1):
    '''BevelVirtualCylindricalGearSetISO10300MethodB1

    This is a mastapy class.
    '''

    TYPE = _BEVEL_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B1

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelVirtualCylindricalGearSetISO10300MethodB1.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
