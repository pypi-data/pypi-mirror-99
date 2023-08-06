﻿'''_717.py

SelectedDesignConstraintsCollection
'''


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor
from mastapy.gears.gear_designs import _712
from mastapy.utility import _1156

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_SELECTED_DESIGN_CONSTRAINTS_COLLECTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'SelectedDesignConstraintsCollection')


__docformat__ = 'restructuredtext en'
__all__ = ('SelectedDesignConstraintsCollection',)


class SelectedDesignConstraintsCollection(_1156.PerMachineSettings):
    '''SelectedDesignConstraintsCollection

    This is a mastapy class.
    '''

    TYPE = _SELECTED_DESIGN_CONSTRAINTS_COLLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SelectedDesignConstraintsCollection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_constraints_database(self) -> 'str':
        '''str: 'DesignConstraintsDatabase' is the original name of this property.'''

        return self.wrapped.DesignConstraintsDatabase.SelectedItemName

    @design_constraints_database.setter
    def design_constraints_database(self, value: 'str'):
        self.wrapped.DesignConstraintsDatabase.SetSelectedItem(str(value) if value else None)

    @property
    def design_constraints(self) -> '_712.DesignConstraintsCollection':
        '''DesignConstraintsCollection: 'DesignConstraints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_712.DesignConstraintsCollection)(self.wrapped.DesignConstraints) if self.wrapped.DesignConstraints else None
