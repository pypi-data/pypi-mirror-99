﻿'''_944.py

CylindricalGearDesignConstraints
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _943
from mastapy._internal import constructor, conversion
from mastapy.utility.databases import _1556
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraints')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraints',)


class CylindricalGearDesignConstraints(_1556.NamedDatabaseItem):
    '''CylindricalGearDesignConstraints

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraints.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_constraints(self) -> 'List[_943.CylindricalGearDesignConstraint]':
        '''List[CylindricalGearDesignConstraint]: 'DesignConstraints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignConstraints, constructor.new(_943.CylindricalGearDesignConstraint))
        return value
