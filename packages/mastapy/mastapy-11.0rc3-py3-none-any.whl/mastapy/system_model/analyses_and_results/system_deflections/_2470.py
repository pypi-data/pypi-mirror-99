﻿'''_2470.py

ShaftSystemDeflection
'''


from typing import Iterable, List

from PIL.Image import Image

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2158
from mastapy.system_model.analyses_and_results.static_loads import _6588
from mastapy.system_model.analyses_and_results.power_flows import _3795
from mastapy.system_model.analyses_and_results.system_deflections import _2468, _2469, _2360
from mastapy.shafts import _19
from mastapy.math_utility.measured_vectors import _1323
from mastapy._internal.python_net import python_net_import

_SHAFT_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ShaftSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSystemDeflection',)


class ShaftSystemDeflection(_2360.AbstractShaftSystemDeflection):
    '''ShaftSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def first_node_deflection_linear(self) -> 'Vector3D':
        '''Vector3D: 'FirstNodeDeflectionLinear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.FirstNodeDeflectionLinear)
        return value

    @property
    def first_node_deflection_angular(self) -> 'Vector3D':
        '''Vector3D: 'FirstNodeDeflectionAngular' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.FirstNodeDeflectionAngular)
        return value

    @property
    def flexible_pin_additional_deflection_amplitude(self) -> 'Iterable[Vector3D]':
        '''Iterable[Vector3D]: 'FlexiblePinAdditionalDeflectionAmplitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_iterable(self.wrapped.FlexiblePinAdditionalDeflectionAmplitude, Vector3D)
        return value

    @property
    def number_of_cycles_for_fatigue(self) -> 'float':
        '''float: 'NumberOfCyclesForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfCyclesForFatigue

    @property
    def pin_tangential_oscillation_amplitude(self) -> 'float':
        '''float: 'PinTangentialOscillationAmplitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinTangentialOscillationAmplitude

    @property
    def two_d_drawing_showing_axial_forces_with_mounted_components(self) -> 'Image':
        '''Image: 'TwoDDrawingShowingAxialForcesWithMountedComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_smt_bitmap(self.wrapped.TwoDDrawingShowingAxialForcesWithMountedComponents)
        return value

    @property
    def component_design(self) -> '_2158.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2158.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6588.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6588.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3795.ShaftPowerFlow':
        '''ShaftPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3795.ShaftPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def shaft_section_end_with_worst_static_safety_factor(self) -> '_2468.ShaftSectionEndResultsSystemDeflection':
        '''ShaftSectionEndResultsSystemDeflection: 'ShaftSectionEndWithWorstStaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2468.ShaftSectionEndResultsSystemDeflection)(self.wrapped.ShaftSectionEndWithWorstStaticSafetyFactor) if self.wrapped.ShaftSectionEndWithWorstStaticSafetyFactor else None

    @property
    def shaft_section_end_with_worst_fatigue_safety_factor(self) -> '_2468.ShaftSectionEndResultsSystemDeflection':
        '''ShaftSectionEndResultsSystemDeflection: 'ShaftSectionEndWithWorstFatigueSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2468.ShaftSectionEndResultsSystemDeflection)(self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactor) if self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactor else None

    @property
    def shaft_section_end_with_worst_fatigue_safety_factor_for_infinite_life(self) -> '_2468.ShaftSectionEndResultsSystemDeflection':
        '''ShaftSectionEndResultsSystemDeflection: 'ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2468.ShaftSectionEndResultsSystemDeflection)(self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife) if self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife else None

    @property
    def component_detailed_analysis(self) -> '_19.ShaftDamageResults':
        '''ShaftDamageResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_19.ShaftDamageResults)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def planetaries(self) -> 'List[ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftSystemDeflection))
        return value

    @property
    def shaft_section_results(self) -> 'List[_2469.ShaftSectionSystemDeflection]':
        '''List[ShaftSectionSystemDeflection]: 'ShaftSectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftSectionResults, constructor.new(_2469.ShaftSectionSystemDeflection))
        return value

    @property
    def shaft_section_end_results_by_offset_with_worst_safety_factor(self) -> 'List[_2468.ShaftSectionEndResultsSystemDeflection]':
        '''List[ShaftSectionEndResultsSystemDeflection]: 'ShaftSectionEndResultsByOffsetWithWorstSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftSectionEndResultsByOffsetWithWorstSafetyFactor, constructor.new(_2468.ShaftSectionEndResultsSystemDeflection))
        return value

    @property
    def mounted_components_applying_torque(self) -> 'List[_1323.ForceResults]':
        '''List[ForceResults]: 'MountedComponentsApplyingTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MountedComponentsApplyingTorque, constructor.new(_1323.ForceResults))
        return value

    def calculate_outer_diameter_to_achieve_fatigue_safety_factor_requirement(self):
        ''' 'CalculateOuterDiameterToAchieveFatigueSafetyFactorRequirement' is the original name of this method.'''

        self.wrapped.CalculateOuterDiameterToAchieveFatigueSafetyFactorRequirement()
