﻿'''_5199.py

BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.mbd_analyses import _5049
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5196
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis',)


class BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis(_5196.BevelDifferentialGearCompoundMultibodyDynamicsAnalysis):
    '''BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_5049.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]':
        '''List[BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5049.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5049.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]':
        '''List[BevelDifferentialPlanetGearMultibodyDynamicsAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5049.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis))
        return value
