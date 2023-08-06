﻿'''_3813.py

ConceptGearMeshModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.gears import _1922
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6146
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3838
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ConceptGearMeshModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshModalAnalysesAtStiffnesses',)


class ConceptGearMeshModalAnalysesAtStiffnesses(_3838.GearMeshModalAnalysesAtStiffnesses):
    '''ConceptGearMeshModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1922.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1922.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6146.ConceptGearMeshLoadCase':
        '''ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6146.ConceptGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
