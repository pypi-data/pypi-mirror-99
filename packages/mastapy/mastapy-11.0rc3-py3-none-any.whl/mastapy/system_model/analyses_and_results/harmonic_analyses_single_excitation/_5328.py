﻿'''_5328.py

ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.couplings import _2228
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6437
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5339
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation',)


class ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation(_5339.CouplingHalfHarmonicAnalysisOfSingleExcitation):
    '''ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2228.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6437.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6437.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
