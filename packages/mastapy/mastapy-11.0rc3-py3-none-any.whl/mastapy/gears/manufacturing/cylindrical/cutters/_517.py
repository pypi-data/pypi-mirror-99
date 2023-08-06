﻿'''_517.py

CylindricalWormGrinderDatabase
'''


from mastapy.gears.manufacturing.cylindrical import _392
from mastapy.gears.manufacturing.cylindrical.cutters import _508
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_WORM_GRINDER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalWormGrinderDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalWormGrinderDatabase',)


class CylindricalWormGrinderDatabase(_392.CylindricalCutterDatabase['_508.CylindricalGearGrindingWorm']):
    '''CylindricalWormGrinderDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_WORM_GRINDER_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalWormGrinderDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
