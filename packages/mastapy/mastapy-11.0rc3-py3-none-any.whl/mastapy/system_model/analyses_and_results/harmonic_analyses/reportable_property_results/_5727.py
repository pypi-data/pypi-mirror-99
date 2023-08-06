﻿'''_5727.py

HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5734, _5729
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_COMPONENT_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic',)


class HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic(_5729.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic):
    '''HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_COMPONENT_WITHIN_A_HARMONIC

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_name(self) -> 'str':
        '''str: 'ComponentName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ComponentName

    @property
    def kinetic_energy(self) -> '_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'KineticEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)(self.wrapped.KineticEnergy) if self.wrapped.KineticEnergy else None

    @property
    def strain_energy(self) -> '_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'StrainEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)(self.wrapped.StrainEnergy) if self.wrapped.StrainEnergy else None

    @property
    def dynamic_mesh_force(self) -> '_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'DynamicMeshForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)(self.wrapped.DynamicMeshForce) if self.wrapped.DynamicMeshForce else None

    @property
    def dynamic_mesh_moment(self) -> '_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'DynamicMeshMoment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5734.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)(self.wrapped.DynamicMeshMoment) if self.wrapped.DynamicMeshMoment else None
