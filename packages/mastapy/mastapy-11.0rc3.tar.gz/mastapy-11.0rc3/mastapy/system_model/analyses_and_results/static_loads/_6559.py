﻿'''_6559.py

MassDiscLoadCase
'''


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.part_model import _2139
from mastapy.system_model.analyses_and_results.static_loads import _6622
from mastapy._internal.python_net import python_net_import

_MASS_DISC_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'MassDiscLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscLoadCase',)


class MassDiscLoadCase(_6622.VirtualComponentLoadCase):
    '''MassDiscLoadCase

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def polar_inertia(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PolarInertia' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PolarInertia) if self.wrapped.PolarInertia else None

    @polar_inertia.setter
    def polar_inertia(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.PolarInertia = value

    @property
    def transverse_inertia(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TransverseInertia' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TransverseInertia) if self.wrapped.TransverseInertia else None

    @transverse_inertia.setter
    def transverse_inertia(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.TransverseInertia = value

    @property
    def mass(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Mass' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Mass) if self.wrapped.Mass else None

    @mass.setter
    def mass(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Mass = value

    @property
    def number_of_nodes_for_node_model(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfNodesForNodeModel' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfNodesForNodeModel) if self.wrapped.NumberOfNodesForNodeModel else None

    @number_of_nodes_for_node_model.setter
    def number_of_nodes_for_node_model(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfNodesForNodeModel = value

    @property
    def component_design(self) -> '_2139.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
