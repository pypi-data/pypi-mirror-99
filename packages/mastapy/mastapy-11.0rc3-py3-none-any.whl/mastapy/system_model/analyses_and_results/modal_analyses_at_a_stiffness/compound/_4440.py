﻿'''_4440.py

MeasurementComponentCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2140
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4311
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4486
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'MeasurementComponentCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundModalAnalysisAtAStiffness',)


class MeasurementComponentCompoundModalAnalysisAtAStiffness(_4486.VirtualComponentCompoundModalAnalysisAtAStiffness):
    '''MeasurementComponentCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2140.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2140.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4311.MeasurementComponentModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentModalAnalysisAtAStiffness]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4311.MeasurementComponentModalAnalysisAtAStiffness))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4311.MeasurementComponentModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentModalAnalysisAtAStiffness]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4311.MeasurementComponentModalAnalysisAtAStiffness))
        return value
