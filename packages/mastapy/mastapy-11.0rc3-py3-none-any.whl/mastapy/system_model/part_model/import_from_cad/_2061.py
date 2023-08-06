﻿'''_2061.py

CylindricalPlanetGearFromCAD
'''


from mastapy.system_model.part_model.import_from_cad import _2060
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'CylindricalPlanetGearFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearFromCAD',)


class CylindricalPlanetGearFromCAD(_2060.CylindricalGearInPlanetarySetFromCAD):
    '''CylindricalPlanetGearFromCAD

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_FROM_CAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
