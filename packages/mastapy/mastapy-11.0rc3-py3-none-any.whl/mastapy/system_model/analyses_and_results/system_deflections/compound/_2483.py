﻿'''_2483.py

KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1936
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2341
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2480
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection',)


class KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection(_2480.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection):
    '''KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1936.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1936.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1936.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1936.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2341.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2341.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2341.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2341.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection))
        return value
