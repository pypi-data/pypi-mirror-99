﻿'''_4400.py

ZerolBevelGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2152
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6284
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4399, _4398, _4294
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ZerolBevelGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetModalAnalysisAtAStiffness',)


class ZerolBevelGearSetModalAnalysisAtAStiffness(_4294.BevelGearSetModalAnalysisAtAStiffness):
    '''ZerolBevelGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2152.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2152.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6284.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6284.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4399.ZerolBevelGearModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearModalAnalysisAtAStiffness]: 'ZerolBevelGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsModalAnalysisAtAStiffness, constructor.new(_4399.ZerolBevelGearModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4398.ZerolBevelGearMeshModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearMeshModalAnalysisAtAStiffness]: 'ZerolBevelMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesModalAnalysisAtAStiffness, constructor.new(_4398.ZerolBevelGearMeshModalAnalysisAtAStiffness))
        return value
