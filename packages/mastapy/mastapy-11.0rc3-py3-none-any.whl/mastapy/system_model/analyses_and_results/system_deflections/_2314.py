﻿'''_2314.py

CylindricalGearMeshSystemDeflectionWithLTCAResults
'''


from mastapy.gears.ltca.cylindrical import _628
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2312
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalGearMeshSystemDeflectionWithLTCAResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshSystemDeflectionWithLTCAResults',)


class CylindricalGearMeshSystemDeflectionWithLTCAResults(_2312.CylindricalGearMeshSystemDeflection):
    '''CylindricalGearMeshSystemDeflectionWithLTCAResults

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def basic_ltca_results(self) -> '_628.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'BasicLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_628.CylindricalGearMeshLoadDistributionAnalysis)(self.wrapped.BasicLTCAResults) if self.wrapped.BasicLTCAResults else None

    @property
    def basic_ltca_results_only_first_planetary_mesh(self) -> '_628.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'BasicLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_628.CylindricalGearMeshLoadDistributionAnalysis)(self.wrapped.BasicLTCAResultsOnlyFirstPlanetaryMesh) if self.wrapped.BasicLTCAResultsOnlyFirstPlanetaryMesh else None

    @property
    def advanced_ltca_results(self) -> '_628.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'AdvancedLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_628.CylindricalGearMeshLoadDistributionAnalysis)(self.wrapped.AdvancedLTCAResults) if self.wrapped.AdvancedLTCAResults else None

    @property
    def advanced_ltca_results_only_first_planetary_mesh(self) -> '_628.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'AdvancedLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_628.CylindricalGearMeshLoadDistributionAnalysis)(self.wrapped.AdvancedLTCAResultsOnlyFirstPlanetaryMesh) if self.wrapped.AdvancedLTCAResultsOnlyFirstPlanetaryMesh else None
