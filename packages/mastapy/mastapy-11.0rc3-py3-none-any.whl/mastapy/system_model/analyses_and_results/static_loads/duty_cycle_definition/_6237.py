﻿'''_6237.py

DesignStateOptions
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.load_case_groups import _5254
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model import _1813
from mastapy.utility_gui import _1504
from mastapy._internal.python_net import python_net_import

_DESIGN_STATE_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'DesignStateOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignStateOptions',)


class DesignStateOptions(_1504.ColumnInputOptions):
    '''DesignStateOptions

    This is a mastapy class.
    '''

    TYPE = _DESIGN_STATE_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignStateOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def create_new_design_state(self) -> 'bool':
        '''bool: 'CreateNewDesignState' is the original name of this property.'''

        return self.wrapped.CreateNewDesignState

    @create_new_design_state.setter
    def create_new_design_state(self, value: 'bool'):
        self.wrapped.CreateNewDesignState = bool(value) if value else False

    @property
    def design_state(self) -> 'list_with_selected_item.ListWithSelectedItem_DesignState':
        '''list_with_selected_item.ListWithSelectedItem_DesignState: 'DesignState' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_DesignState)(self.wrapped.DesignState) if self.wrapped.DesignState else None

    @design_state.setter
    def design_state(self, value: 'list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_DesignState.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.DesignState = value

    @property
    def design_state_destinations(self) -> 'List[_1813.DutyCycleImporterDesignEntityMatch[_5254.DesignState]]':
        '''List[DutyCycleImporterDesignEntityMatch[DesignState]]: 'DesignStateDestinations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignStateDestinations, constructor.new(_1813.DutyCycleImporterDesignEntityMatch)[_5254.DesignState])
        return value
