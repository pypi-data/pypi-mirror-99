﻿'''_5694.py

MeasurementComponentHarmonicAnalysis
'''


from mastapy.system_model.part_model import _2140
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6560
from mastapy.system_model.analyses_and_results.system_deflections import _2446
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5744
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'MeasurementComponentHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentHarmonicAnalysis',)


class MeasurementComponentHarmonicAnalysis(_5744.VirtualComponentHarmonicAnalysis):
    '''MeasurementComponentHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentHarmonicAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2446.MeasurementComponentSystemDeflection':
        '''MeasurementComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2446.MeasurementComponentSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
