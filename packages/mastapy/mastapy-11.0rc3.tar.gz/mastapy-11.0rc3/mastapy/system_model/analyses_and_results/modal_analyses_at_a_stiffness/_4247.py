﻿'''_4247.py

BevelDifferentialGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2191
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6460
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4246, _4245, _4252
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'BevelDifferentialGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetModalAnalysisAtAStiffness',)


class BevelDifferentialGearSetModalAnalysisAtAStiffness(_4252.BevelGearSetModalAnalysisAtAStiffness):
    '''BevelDifferentialGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2191.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6460.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6460.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4246.BevelDifferentialGearModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearModalAnalysisAtAStiffness]: 'BevelDifferentialGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsModalAnalysisAtAStiffness, constructor.new(_4246.BevelDifferentialGearModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4245.BevelDifferentialGearMeshModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearMeshModalAnalysisAtAStiffness]: 'BevelDifferentialMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesModalAnalysisAtAStiffness, constructor.new(_4245.BevelDifferentialGearMeshModalAnalysisAtAStiffness))
        return value
