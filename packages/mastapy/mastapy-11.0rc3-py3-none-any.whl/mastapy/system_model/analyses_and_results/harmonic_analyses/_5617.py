﻿'''_5617.py

ClutchHarmonicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6470
from mastapy.system_model.analyses_and_results.system_deflections import _2381
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5634
from mastapy._internal.python_net import python_net_import

_CLUTCH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ClutchHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHarmonicAnalysis',)


class ClutchHarmonicAnalysis(_5634.CouplingHarmonicAnalysis):
    '''ClutchHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2253.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6470.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6470.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2381.ClutchSystemDeflection':
        '''ClutchSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2381.ClutchSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
