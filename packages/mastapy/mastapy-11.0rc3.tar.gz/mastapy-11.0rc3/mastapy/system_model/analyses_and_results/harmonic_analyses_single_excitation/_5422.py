﻿'''_5422.py

PowerLoadHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model import _2149
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6577
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5457
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'PowerLoadHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadHarmonicAnalysisOfSingleExcitation',)


class PowerLoadHarmonicAnalysisOfSingleExcitation(_5457.VirtualComponentHarmonicAnalysisOfSingleExcitation):
    '''PowerLoadHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2149.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6577.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6577.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
