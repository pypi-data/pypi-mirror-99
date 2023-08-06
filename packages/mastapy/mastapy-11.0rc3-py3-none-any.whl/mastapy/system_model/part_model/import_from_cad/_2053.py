﻿'''_2053.py

AbstractShaftFromCAD
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2055
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'AbstractShaftFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftFromCAD',)


class AbstractShaftFromCAD(_2055.ComponentFromCAD):
    '''AbstractShaftFromCAD

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_FROM_CAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.'''

        return self.wrapped.Offset

    @offset.setter
    def offset(self, value: 'float'):
        self.wrapped.Offset = float(value) if value else 0.0
