﻿'''_5636.py

CVTHarmonicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2261
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2402
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5604
from mastapy._internal.python_net import python_net_import

_CVT_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'CVTHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTHarmonicAnalysis',)


class CVTHarmonicAnalysis(_5604.BeltDriveHarmonicAnalysis):
    '''CVTHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2261.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2261.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def system_deflection_results(self) -> '_2402.CVTSystemDeflection':
        '''CVTSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2402.CVTSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
