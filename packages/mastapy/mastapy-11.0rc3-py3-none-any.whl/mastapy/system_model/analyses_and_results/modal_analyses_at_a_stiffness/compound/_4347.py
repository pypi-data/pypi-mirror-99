﻿'''_4347.py

BevelGearCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4335
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'BevelGearCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearCompoundModalAnalysisAtAStiffness',)


class BevelGearCompoundModalAnalysisAtAStiffness(_4335.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness):
    '''BevelGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
