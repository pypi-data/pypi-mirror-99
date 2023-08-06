﻿'''_573.py

CylindricalShaperDatabase
'''


from mastapy.gears.manufacturing.cylindrical import _557
from mastapy.gears.manufacturing.cylindrical.cutters import _679
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_SHAPER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalShaperDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalShaperDatabase',)


class CylindricalShaperDatabase(_557.CylindricalCutterDatabase['_679.CylindricalGearShaper']):
    '''CylindricalShaperDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_SHAPER_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalShaperDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
