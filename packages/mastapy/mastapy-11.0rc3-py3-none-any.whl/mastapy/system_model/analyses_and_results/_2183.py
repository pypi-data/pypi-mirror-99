﻿'''_2183.py

DynamicModelforSteadyStateSynchronousResponseAnalysis
'''


from mastapy.system_model.analyses_and_results import _2175
from mastapy._internal.python_net import python_net_import

_DYNAMIC_MODELFOR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DynamicModelforSteadyStateSynchronousResponseAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicModelforSteadyStateSynchronousResponseAnalysis',)


class DynamicModelforSteadyStateSynchronousResponseAnalysis(_2175.SingleAnalysis):
    '''DynamicModelforSteadyStateSynchronousResponseAnalysis

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_MODELFOR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicModelforSteadyStateSynchronousResponseAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
