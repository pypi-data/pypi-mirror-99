﻿'''_4475.py

StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4346
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4469
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness',)


class StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness(_4469.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness):
    '''StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_4346.StraightBevelPlanetGearModalAnalysisAtAStiffness]':
        '''List[StraightBevelPlanetGearModalAnalysisAtAStiffness]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4346.StraightBevelPlanetGearModalAnalysisAtAStiffness))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4346.StraightBevelPlanetGearModalAnalysisAtAStiffness]':
        '''List[StraightBevelPlanetGearModalAnalysisAtAStiffness]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4346.StraightBevelPlanetGearModalAnalysisAtAStiffness))
        return value
