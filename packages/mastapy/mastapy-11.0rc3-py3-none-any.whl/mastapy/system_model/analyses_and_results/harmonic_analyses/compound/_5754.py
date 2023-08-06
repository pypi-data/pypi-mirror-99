﻿'''_5754.py

BevelDifferentialGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2162
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5752, _5753, _5759
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5574
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'BevelDifferentialGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundHarmonicAnalysis',)


class BevelDifferentialGearSetCompoundHarmonicAnalysis(_5759.BevelGearSetCompoundHarmonicAnalysis):
    '''BevelDifferentialGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2162.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2162.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2162.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2162.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_harmonic_analysis(self) -> 'List[_5752.BevelDifferentialGearCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearCompoundHarmonicAnalysis]: 'BevelDifferentialGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundHarmonicAnalysis, constructor.new(_5752.BevelDifferentialGearCompoundHarmonicAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_harmonic_analysis(self) -> 'List[_5753.BevelDifferentialGearMeshCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundHarmonicAnalysis]: 'BevelDifferentialMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundHarmonicAnalysis, constructor.new(_5753.BevelDifferentialGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5574.BevelDifferentialGearSetHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5574.BevelDifferentialGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5574.BevelDifferentialGearSetHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5574.BevelDifferentialGearSetHarmonicAnalysis))
        return value
