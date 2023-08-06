﻿'''_4952.py

CylindricalGearMeshCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1989
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4799
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4963
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CylindricalGearMeshCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundModalAnalysis',)


class CylindricalGearMeshCompoundModalAnalysis(_4963.GearMeshCompoundModalAnalysis):
    '''CylindricalGearMeshCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1989.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1989.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4799.CylindricalGearMeshModalAnalysis]':
        '''List[CylindricalGearMeshModalAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_4799.CylindricalGearMeshModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundModalAnalysis]':
        '''List[CylindricalGearMeshCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundModalAnalysis))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4799.CylindricalGearMeshModalAnalysis]':
        '''List[CylindricalGearMeshModalAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_4799.CylindricalGearMeshModalAnalysis))
        return value
