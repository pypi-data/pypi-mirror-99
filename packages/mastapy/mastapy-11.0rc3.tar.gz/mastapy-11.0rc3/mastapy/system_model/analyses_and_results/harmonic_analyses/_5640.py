﻿'''_5640.py

CycloidalDiscHarmonicAnalysis
'''


from mastapy.system_model.part_model.cycloidal import _2244
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6494
from mastapy.system_model.analyses_and_results.system_deflections import _2406
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5595
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'CycloidalDiscHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscHarmonicAnalysis',)


class CycloidalDiscHarmonicAnalysis(_5595.AbstractShaftHarmonicAnalysis):
    '''CycloidalDiscHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2244.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6494.CycloidalDiscLoadCase':
        '''CycloidalDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6494.CycloidalDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2406.CycloidalDiscSystemDeflection':
        '''CycloidalDiscSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2406.CycloidalDiscSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
