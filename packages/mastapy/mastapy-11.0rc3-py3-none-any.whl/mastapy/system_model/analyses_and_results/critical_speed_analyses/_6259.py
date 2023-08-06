﻿'''_6259.py

MeasurementComponentCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model import _2140
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6560
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6305
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'MeasurementComponentCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCriticalSpeedAnalysis',)


class MeasurementComponentCriticalSpeedAnalysis(_6305.VirtualComponentCriticalSpeedAnalysis):
    '''MeasurementComponentCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCriticalSpeedAnalysis.TYPE'):
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
    def component_load_case(self) -> '_6560.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6560.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
