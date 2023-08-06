﻿'''_3578.py

DutyCycleResultsForSingleShaft
'''


from mastapy.shafts import _18
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_RESULTS_FOR_SINGLE_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DutyCycleResultsForSingleShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleResultsForSingleShaft',)


class DutyCycleResultsForSingleShaft(_0.APIBase):
    '''DutyCycleResultsForSingleShaft

    This is a mastapy class.
    '''

    TYPE = _DUTY_CYCLE_RESULTS_FOR_SINGLE_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DutyCycleResultsForSingleShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_results(self) -> '_18.ShaftDamageResults':
        '''ShaftDamageResults: 'DutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_18.ShaftDamageResults)(self.wrapped.DutyCycleResults) if self.wrapped.DutyCycleResults else None
