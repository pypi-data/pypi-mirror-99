﻿'''_366.py

BevelGearAbstractMaterialDatabase
'''


from typing import Generic, TypeVar

from mastapy.materials import _74
from mastapy.gears.materials import _369
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_ABSTRACT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'BevelGearAbstractMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearAbstractMaterialDatabase',)


T = TypeVar('T', bound='_369.BevelGearMaterial')


class BevelGearAbstractMaterialDatabase(_74.MaterialDatabase['T'], Generic[T]):
    '''BevelGearAbstractMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _BEVEL_GEAR_ABSTRACT_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearAbstractMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
