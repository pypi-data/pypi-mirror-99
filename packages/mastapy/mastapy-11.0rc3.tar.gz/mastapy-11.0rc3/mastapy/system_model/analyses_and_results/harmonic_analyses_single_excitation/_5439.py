﻿'''_5439.py

SpringDamperHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2275
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6597
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5373
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'SpringDamperHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHarmonicAnalysisOfSingleExcitation',)


class SpringDamperHarmonicAnalysisOfSingleExcitation(_5373.CouplingHarmonicAnalysisOfSingleExcitation):
    '''SpringDamperHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2275.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6597.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6597.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
