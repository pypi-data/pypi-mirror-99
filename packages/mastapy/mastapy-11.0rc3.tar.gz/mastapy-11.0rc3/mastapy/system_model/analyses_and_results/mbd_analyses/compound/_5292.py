﻿'''_5292.py

StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2221
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5290, _5291, _5203
from mastapy.system_model.analyses_and_results.mbd_analyses import _5154
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis',)


class StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis(_5203.BevelGearSetCompoundMultibodyDynamicsAnalysis):
    '''StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2221.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2221.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_multibody_dynamics_analysis(self) -> 'List[_5290.StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis]: 'StraightBevelDiffGearsCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundMultibodyDynamicsAnalysis, constructor.new(_5290.StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_compound_multibody_dynamics_analysis(self) -> 'List[_5291.StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis]: 'StraightBevelDiffMeshesCompoundMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundMultibodyDynamicsAnalysis, constructor.new(_5291.StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5154.StraightBevelDiffGearSetMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5154.StraightBevelDiffGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5154.StraightBevelDiffGearSetMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5154.StraightBevelDiffGearSetMultibodyDynamicsAnalysis))
        return value
