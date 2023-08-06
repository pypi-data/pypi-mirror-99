﻿'''_5693.py

MassDiscHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2139
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6559
from mastapy.system_model.analyses_and_results.system_deflections import _2445
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5744
from mastapy._internal.python_net import python_net_import

_MASS_DISC_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'MassDiscHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscHarmonicAnalysis',)


class MassDiscHarmonicAnalysis(_5744.VirtualComponentHarmonicAnalysis):
    '''MassDiscHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2139.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6559.MassDiscLoadCase':
        '''MassDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6559.MassDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2445.MassDiscSystemDeflection':
        '''MassDiscSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2445.MassDiscSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[MassDiscHarmonicAnalysis]':
        '''List[MassDiscHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscHarmonicAnalysis))
        return value
