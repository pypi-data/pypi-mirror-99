﻿'''_4642.py

BoltedJointCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2121
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4512
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4720
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'BoltedJointCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundModalAnalysisAtASpeed',)


class BoltedJointCompoundModalAnalysisAtASpeed(_4720.SpecialisedAssemblyCompoundModalAnalysisAtASpeed):
    '''BoltedJointCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2121.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2121.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4512.BoltedJointModalAnalysisAtASpeed]':
        '''List[BoltedJointModalAnalysisAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4512.BoltedJointModalAnalysisAtASpeed))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4512.BoltedJointModalAnalysisAtASpeed]':
        '''List[BoltedJointModalAnalysisAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4512.BoltedJointModalAnalysisAtASpeed))
        return value
