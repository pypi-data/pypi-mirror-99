﻿'''_823.py

ConicalMeshLoadCase
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.conical import _1061, _1071
from mastapy.gears.load_case import _811
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.LoadCase.Conical', 'ConicalMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshLoadCase',)


class ConicalMeshLoadCase(_811.MeshLoadCase):
    '''ConicalMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def use_user_specified_misalignments_in_tca(self) -> 'bool':
        '''bool: 'UseUserSpecifiedMisalignmentsInTCA' is the original name of this property.'''

        return self.wrapped.UseUserSpecifiedMisalignmentsInTCA

    @use_user_specified_misalignments_in_tca.setter
    def use_user_specified_misalignments_in_tca(self, value: 'bool'):
        self.wrapped.UseUserSpecifiedMisalignmentsInTCA = bool(value) if value else False

    @property
    def active_flank(self) -> '_1061.ActiveConicalFlank':
        '''ActiveConicalFlank: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ActiveFlank)
        return constructor.new(_1061.ActiveConicalFlank)(value) if value else None

    @property
    def misalignments_total(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MisalignmentsTotal) if self.wrapped.MisalignmentsTotal else None

    @property
    def misalignments_pinion(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MisalignmentsPinion) if self.wrapped.MisalignmentsPinion else None

    @property
    def misalignments_wheel(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWheel) if self.wrapped.MisalignmentsWheel else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_total(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal) if self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_pinion(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion) if self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_wheel(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel) if self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel else None

    @property
    def mesh_node_misalignments_total(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MeshNodeMisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MeshNodeMisalignmentsTotal) if self.wrapped.MeshNodeMisalignmentsTotal else None

    @property
    def mesh_node_misalignments_pinion(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MeshNodeMisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MeshNodeMisalignmentsPinion) if self.wrapped.MeshNodeMisalignmentsPinion else None

    @property
    def mesh_node_misalignments_wheel(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MeshNodeMisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.MeshNodeMisalignmentsWheel) if self.wrapped.MeshNodeMisalignmentsWheel else None

    @property
    def user_specified_misalignments(self) -> '_1071.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'UserSpecifiedMisalignments' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.ConicalMeshMisalignments)(self.wrapped.UserSpecifiedMisalignments) if self.wrapped.UserSpecifiedMisalignments else None
