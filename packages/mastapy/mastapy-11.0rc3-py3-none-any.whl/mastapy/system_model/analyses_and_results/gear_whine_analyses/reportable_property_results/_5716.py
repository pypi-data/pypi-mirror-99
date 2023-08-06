﻿'''_5716.py

SingleWhineAnalysisResultsPropertyAccessor
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.reportable_property_results import _5712
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'SingleWhineAnalysisResultsPropertyAccessor')


__docformat__ = 'restructuredtext en'
__all__ = ('SingleWhineAnalysisResultsPropertyAccessor',)


class SingleWhineAnalysisResultsPropertyAccessor(_0.APIBase):
    '''SingleWhineAnalysisResultsPropertyAccessor

    This is a mastapy class.
    '''

    TYPE = _SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SingleWhineAnalysisResultsPropertyAccessor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def orders(self) -> 'List[_5712.ResultsForOrder]':
        '''List[ResultsForOrder]: 'Orders' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Orders, constructor.new(_5712.ResultsForOrder))
        return value
