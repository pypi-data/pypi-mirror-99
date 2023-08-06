﻿'''_942.py

ConicalSetFEModel
'''


from mastapy.nodal_analysis import _1386
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.fe_model.conical import _943
from mastapy._internal.implicit import list_with_selected_item
from mastapy.gears.manufacturing.bevel import _573
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.fe_model import _936
from mastapy._internal.python_net import python_net_import

_CONICAL_SET_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel.Conical', 'ConicalSetFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalSetFEModel',)


class ConicalSetFEModel(_936.GearSetFEModel):
    '''ConicalSetFEModel

    This is a mastapy class.
    '''

    TYPE = _CONICAL_SET_FE_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalSetFEModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def element_order(self) -> '_1386.ElementOrder':
        '''ElementOrder: 'ElementOrder' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ElementOrder)
        return constructor.new(_1386.ElementOrder)(value) if value else None

    @element_order.setter
    def element_order(self, value: '_1386.ElementOrder'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ElementOrder = value

    @property
    def flank_data_source(self) -> '_943.FlankDataSource':
        '''FlankDataSource: 'FlankDataSource' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FlankDataSource)
        return constructor.new(_943.FlankDataSource)(value) if value else None

    @flank_data_source.setter
    def flank_data_source(self, value: '_943.FlankDataSource'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FlankDataSource = value

    @property
    def selected_design(self) -> 'list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig':
        '''list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig: 'SelectedDesign' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig)(self.wrapped.SelectedDesign) if self.wrapped.SelectedDesign else None

    @selected_design.setter
    def selected_design(self, value: 'list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ConicalSetManufacturingConfig.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedDesign = value
