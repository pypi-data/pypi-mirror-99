﻿'''_7152.py

StraightBevelDiffGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2221
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7150, _7151, _7063
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7022
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'StraightBevelDiffGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundAdvancedSystemDeflection',)


class StraightBevelDiffGearSetCompoundAdvancedSystemDeflection(_7063.BevelGearSetCompoundAdvancedSystemDeflection):
    '''StraightBevelDiffGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2221.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2221.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2221.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_advanced_system_deflection(self) -> 'List[_7150.StraightBevelDiffGearCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearCompoundAdvancedSystemDeflection]: 'StraightBevelDiffGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundAdvancedSystemDeflection, constructor.new(_7150.StraightBevelDiffGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_diff_meshes_compound_advanced_system_deflection(self) -> 'List[_7151.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]: 'StraightBevelDiffMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundAdvancedSystemDeflection, constructor.new(_7151.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_7022.StraightBevelDiffGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_7022.StraightBevelDiffGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_7022.StraightBevelDiffGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_7022.StraightBevelDiffGearSetAdvancedSystemDeflection))
        return value
