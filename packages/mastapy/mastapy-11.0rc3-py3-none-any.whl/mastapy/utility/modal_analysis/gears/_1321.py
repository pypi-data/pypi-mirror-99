﻿'''_1321.py

GearOrderForTE
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility.modal_analysis.gears import _1322, _1325, _1327
from mastapy._internal.python_net import python_net_import

_GEAR_ORDER_FOR_TE = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'GearOrderForTE')


__docformat__ = 'restructuredtext en'
__all__ = ('GearOrderForTE',)


class GearOrderForTE(_1327.OrderWithRadius):
    '''GearOrderForTE

    This is a mastapy class.
    '''

    TYPE = _GEAR_ORDER_FOR_TE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearOrderForTE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_teeth(self) -> 'int':
        '''int: 'NumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfTeeth

    @property
    def position(self) -> '_1322.GearPositions':
        '''GearPositions: 'Position' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.Position)
        return constructor.new(_1322.GearPositions)(value) if value else None

    @property
    def additional_orders_and_harmonics(self) -> 'List[_1325.OrderForTE]':
        '''List[OrderForTE]: 'AdditionalOrdersAndHarmonics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AdditionalOrdersAndHarmonics, constructor.new(_1325.OrderForTE))
        return value
