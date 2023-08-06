﻿'''_4887.py

BevelGearCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4875
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BevelGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearCompoundModalAnalysis',)


class BevelGearCompoundModalAnalysis(_4875.AGMAGleasonConicalGearCompoundModalAnalysis):
    '''BevelGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
