﻿'''_2068.py

FESubstructureWithSelectionComponents
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1262
from mastapy._math.vector_3d import Vector3D
from mastapy.system_model.fe.links import _2097
from mastapy.system_model.fe import (
    _2056, _2076, _2048, _2047,
    _2067
)
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
    _182, _184, _183, _179,
    _185, _181, _180, _178
)
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_WITH_SELECTION_COMPONENTS = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureWithSelectionComponents')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureWithSelectionComponents',)


class FESubstructureWithSelectionComponents(_2067.FESubstructureWithSelection):
    '''FESubstructureWithSelectionComponents

    This is a mastapy class.
    '''

    TYPE = _FE_SUBSTRUCTURE_WITH_SELECTION_COMPONENTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FESubstructureWithSelectionComponents.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def radius_of_circle_through_selected_nodes(self) -> 'float':
        '''float: 'RadiusOfCircleThroughSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RadiusOfCircleThroughSelectedNodes

    @property
    def manual_alignment(self) -> '_1262.CoordinateSystemEditor':
        '''CoordinateSystemEditor: 'ManualAlignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1262.CoordinateSystemEditor)(self.wrapped.ManualAlignment) if self.wrapped.ManualAlignment else None

    @property
    def distance_between_selected_nodes(self) -> 'Vector3D':
        '''Vector3D: 'DistanceBetweenSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.DistanceBetweenSelectedNodes)
        return value

    @property
    def midpoint_of_selected_nodes(self) -> 'Vector3D':
        '''Vector3D: 'MidpointOfSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.MidpointOfSelectedNodes)
        return value

    @property
    def centre_of_circle_through_selected_nodes(self) -> 'Vector3D':
        '''Vector3D: 'CentreOfCircleThroughSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.CentreOfCircleThroughSelectedNodes)
        return value

    @property
    def component_links(self) -> 'List[_2097.FELinkWithSelection]':
        '''List[FELinkWithSelection]: 'ComponentLinks' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentLinks, constructor.new(_2097.FELinkWithSelection))
        return value

    @property
    def links_for_selected_component(self) -> 'List[_2097.FELinkWithSelection]':
        '''List[FELinkWithSelection]: 'LinksForSelectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LinksForSelectedComponent, constructor.new(_2097.FELinkWithSelection))
        return value

    @property
    def links_for_electric_machine(self) -> 'List[_2097.FELinkWithSelection]':
        '''List[FELinkWithSelection]: 'LinksForElectricMachine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LinksForElectricMachine, constructor.new(_2097.FELinkWithSelection))
        return value

    @property
    def rigid_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_182.ElementPropertiesRigid]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesRigid]]: 'RigidElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RigidElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_182.ElementPropertiesRigid])
        return value

    @property
    def solid_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_184.ElementPropertiesSolid]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesSolid]]: 'SolidElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SolidElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_184.ElementPropertiesSolid])
        return value

    @property
    def shell_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_183.ElementPropertiesShell]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesShell]]: 'ShellElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShellElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_183.ElementPropertiesShell])
        return value

    @property
    def beam_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_179.ElementPropertiesBeam]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesBeam]]: 'BeamElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeamElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_179.ElementPropertiesBeam])
        return value

    @property
    def spring_dashpot_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_185.ElementPropertiesSpringDashpot]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesSpringDashpot]]: 'SpringDashpotElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDashpotElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_185.ElementPropertiesSpringDashpot])
        return value

    @property
    def mass_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_181.ElementPropertiesMass]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesMass]]: 'MassElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_181.ElementPropertiesMass])
        return value

    @property
    def interface_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_180.ElementPropertiesInterface]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesInterface]]: 'InterfaceElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InterfaceElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_180.ElementPropertiesInterface])
        return value

    @property
    def other_element_properties(self) -> 'List[_2056.ElementPropertiesWithSelection[_178.ElementPropertiesBase]]':
        '''List[ElementPropertiesWithSelection[ElementPropertiesBase]]: 'OtherElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OtherElementProperties, constructor.new(_2056.ElementPropertiesWithSelection)[_178.ElementPropertiesBase])
        return value

    @property
    def materials(self) -> 'List[_2076.MaterialPropertiesWithSelection]':
        '''List[MaterialPropertiesWithSelection]: 'Materials' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Materials, constructor.new(_2076.MaterialPropertiesWithSelection))
        return value

    @property
    def coordinate_systems(self) -> 'List[_2048.CoordinateSystemWithSelection]':
        '''List[CoordinateSystemWithSelection]: 'CoordinateSystems' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CoordinateSystems, constructor.new(_2048.CoordinateSystemWithSelection))
        return value

    @property
    def contact_pairs(self) -> 'List[_2047.ContactPairWithSelection]':
        '''List[ContactPairWithSelection]: 'ContactPairs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ContactPairs, constructor.new(_2047.ContactPairWithSelection))
        return value

    def replace_selected_shaft(self):
        ''' 'ReplaceSelectedShaft' is the original name of this method.'''

        self.wrapped.ReplaceSelectedShaft()

    def auto_select_node_ring(self):
        ''' 'AutoSelectNodeRing' is the original name of this method.'''

        self.wrapped.AutoSelectNodeRing()

    def use_selected_component_for_alignment(self):
        ''' 'UseSelectedComponentForAlignment' is the original name of this method.'''

        self.wrapped.UseSelectedComponentForAlignment()
