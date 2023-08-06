﻿'''_397.py

CylindricalHobDatabase
'''


from mastapy.gears.manufacturing.cylindrical import _392
from mastapy.gears.manufacturing.cylindrical.cutters import _509
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_HOB_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalHobDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalHobDatabase',)


class CylindricalHobDatabase(_392.CylindricalCutterDatabase['_509.CylindricalGearHobDesign']):
    '''CylindricalHobDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_HOB_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalHobDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
