﻿'''_4104.py

ModalAnalysesAtSpeedsOptions
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import _2072
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSES_AT_SPEEDS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ModalAnalysesAtSpeedsOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysesAtSpeedsOptions',)


class ModalAnalysesAtSpeedsOptions(_0.APIBase):
    '''ModalAnalysesAtSpeedsOptions

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSES_AT_SPEEDS_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysesAtSpeedsOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def start_speed(self) -> 'float':
        '''float: 'StartSpeed' is the original name of this property.'''

        return self.wrapped.StartSpeed

    @start_speed.setter
    def start_speed(self, value: 'float'):
        self.wrapped.StartSpeed = float(value) if value else 0.0

    @property
    def end_speed(self) -> 'float':
        '''float: 'EndSpeed' is the original name of this property.'''

        return self.wrapped.EndSpeed

    @end_speed.setter
    def end_speed(self, value: 'float'):
        self.wrapped.EndSpeed = float(value) if value else 0.0

    @property
    def number_of_speeds(self) -> 'int':
        '''int: 'NumberOfSpeeds' is the original name of this property.'''

        return self.wrapped.NumberOfSpeeds

    @number_of_speeds.setter
    def number_of_speeds(self, value: 'int'):
        self.wrapped.NumberOfSpeeds = int(value) if value else 0

    @property
    def number_of_modes(self) -> 'int':
        '''int: 'NumberOfModes' is the original name of this property.'''

        return self.wrapped.NumberOfModes

    @number_of_modes.setter
    def number_of_modes(self, value: 'int'):
        self.wrapped.NumberOfModes = int(value) if value else 0

    @property
    def include_gyroscopic_effects(self) -> 'bool':
        '''bool: 'IncludeGyroscopicEffects' is the original name of this property.'''

        return self.wrapped.IncludeGyroscopicEffects

    @include_gyroscopic_effects.setter
    def include_gyroscopic_effects(self, value: 'bool'):
        self.wrapped.IncludeGyroscopicEffects = bool(value) if value else False

    @property
    def include_damping_effects(self) -> 'bool':
        '''bool: 'IncludeDampingEffects' is the original name of this property.'''

        return self.wrapped.IncludeDampingEffects

    @include_damping_effects.setter
    def include_damping_effects(self, value: 'bool'):
        self.wrapped.IncludeDampingEffects = bool(value) if value else False

    @property
    def reference_power_load(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        '''list_with_selected_item.ListWithSelectedItem_PowerLoad: 'ReferencePowerLoad' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_PowerLoad)(self.wrapped.ReferencePowerLoad) if self.wrapped.ReferencePowerLoad else None

    @reference_power_load.setter
    def reference_power_load(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ReferencePowerLoad = value

    @property
    def sort_modes(self) -> 'bool':
        '''bool: 'SortModes' is the original name of this property.'''

        return self.wrapped.SortModes

    @sort_modes.setter
    def sort_modes(self, value: 'bool'):
        self.wrapped.SortModes = bool(value) if value else False
