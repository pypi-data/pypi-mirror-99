﻿'''_5101.py

HypoidGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2210
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6545
from mastapy.system_model.analyses_and_results.mbd_analyses import _5100, _5099, _5039
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'HypoidGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetMultibodyDynamicsAnalysis',)


class HypoidGearSetMultibodyDynamicsAnalysis(_5039.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis):
    '''HypoidGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2210.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6545.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6545.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5100.HypoidGearMultibodyDynamicsAnalysis]':
        '''List[HypoidGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5100.HypoidGearMultibodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gears_multibody_dynamics_analysis(self) -> 'List[_5100.HypoidGearMultibodyDynamicsAnalysis]':
        '''List[HypoidGearMultibodyDynamicsAnalysis]: 'HypoidGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsMultibodyDynamicsAnalysis, constructor.new(_5100.HypoidGearMultibodyDynamicsAnalysis))
        return value

    @property
    def hypoid_meshes_multibody_dynamics_analysis(self) -> 'List[_5099.HypoidGearMeshMultibodyDynamicsAnalysis]':
        '''List[HypoidGearMeshMultibodyDynamicsAnalysis]: 'HypoidMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesMultibodyDynamicsAnalysis, constructor.new(_5099.HypoidGearMeshMultibodyDynamicsAnalysis))
        return value
