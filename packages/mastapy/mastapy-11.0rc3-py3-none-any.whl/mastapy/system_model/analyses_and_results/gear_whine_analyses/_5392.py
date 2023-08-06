﻿'''_5392.py

GearWhineAnalysisOptions
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _5470
from mastapy.system_model.analyses_and_results.modal_analyses import _4841
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5434, _5383
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearWhineAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisOptions',)


class GearWhineAnalysisOptions(_0.APIBase):
    '''GearWhineAnalysisOptions

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def amplitude_cut_off_for_linear_te(self) -> 'float':
        '''float: 'AmplitudeCutOffForLinearTE' is the original name of this property.'''

        return self.wrapped.AmplitudeCutOffForLinearTE

    @amplitude_cut_off_for_linear_te.setter
    def amplitude_cut_off_for_linear_te(self, value: 'float'):
        self.wrapped.AmplitudeCutOffForLinearTE = float(value) if value else 0.0

    @property
    def amplitude_cut_off_for_misalignment_excitation(self) -> 'float':
        '''float: 'AmplitudeCutOffForMisalignmentExcitation' is the original name of this property.'''

        return self.wrapped.AmplitudeCutOffForMisalignmentExcitation

    @amplitude_cut_off_for_misalignment_excitation.setter
    def amplitude_cut_off_for_misalignment_excitation(self, value: 'float'):
        self.wrapped.AmplitudeCutOffForMisalignmentExcitation = float(value) if value else 0.0

    @property
    def modal_damping_factor(self) -> 'float':
        '''float: 'ModalDampingFactor' is the original name of this property.'''

        return self.wrapped.ModalDampingFactor

    @modal_damping_factor.setter
    def modal_damping_factor(self, value: 'float'):
        self.wrapped.ModalDampingFactor = float(value) if value else 0.0

    @property
    def rayleigh_damping_alpha(self) -> 'float':
        '''float: 'RayleighDampingAlpha' is the original name of this property.'''

        return self.wrapped.RayleighDampingAlpha

    @rayleigh_damping_alpha.setter
    def rayleigh_damping_alpha(self, value: 'float'):
        self.wrapped.RayleighDampingAlpha = float(value) if value else 0.0

    @property
    def rayleigh_damping_beta(self) -> 'float':
        '''float: 'RayleighDampingBeta' is the original name of this property.'''

        return self.wrapped.RayleighDampingBeta

    @rayleigh_damping_beta.setter
    def rayleigh_damping_beta(self, value: 'float'):
        self.wrapped.RayleighDampingBeta = float(value) if value else 0.0

    @property
    def specify_per_mode_damping_factors(self) -> 'bool':
        '''bool: 'SpecifyPerModeDampingFactors' is the original name of this property.'''

        return self.wrapped.SpecifyPerModeDampingFactors

    @specify_per_mode_damping_factors.setter
    def specify_per_mode_damping_factors(self, value: 'bool'):
        self.wrapped.SpecifyPerModeDampingFactors = bool(value) if value else False

    @property
    def number_of_harmonics(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfHarmonics' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfHarmonics) if self.wrapped.NumberOfHarmonics else None

    @number_of_harmonics.setter
    def number_of_harmonics(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfHarmonics = value

    @property
    def crop_to_speed_range_for_export_and_reports(self) -> 'bool':
        '''bool: 'CropToSpeedRangeForExportAndReports' is the original name of this property.'''

        return self.wrapped.CropToSpeedRangeForExportAndReports

    @crop_to_speed_range_for_export_and_reports.setter
    def crop_to_speed_range_for_export_and_reports(self, value: 'bool'):
        self.wrapped.CropToSpeedRangeForExportAndReports = bool(value) if value else False

    @property
    def penalty_mass_for_enforced_te(self) -> 'float':
        '''float: 'PenaltyMassForEnforcedTE' is the original name of this property.'''

        return self.wrapped.PenaltyMassForEnforcedTE

    @penalty_mass_for_enforced_te.setter
    def penalty_mass_for_enforced_te(self, value: 'float'):
        self.wrapped.PenaltyMassForEnforcedTE = float(value) if value else 0.0

    @property
    def penalty_stiffness_for_enforced_te(self) -> 'float':
        '''float: 'PenaltyStiffnessForEnforcedTE' is the original name of this property.'''

        return self.wrapped.PenaltyStiffnessForEnforcedTE

    @penalty_stiffness_for_enforced_te.setter
    def penalty_stiffness_for_enforced_te(self, value: 'float'):
        self.wrapped.PenaltyStiffnessForEnforcedTE = float(value) if value else 0.0

    @property
    def calculate_uncoupled_modes_during_analysis(self) -> 'bool':
        '''bool: 'CalculateUncoupledModesDuringAnalysis' is the original name of this property.'''

        return self.wrapped.CalculateUncoupledModesDuringAnalysis

    @calculate_uncoupled_modes_during_analysis.setter
    def calculate_uncoupled_modes_during_analysis(self, value: 'bool'):
        self.wrapped.CalculateUncoupledModesDuringAnalysis = bool(value) if value else False

    @property
    def excitation_selection(self) -> '_5470.ExcitationSourceSelectionGroup':
        '''ExcitationSourceSelectionGroup: 'ExcitationSelection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5470.ExcitationSourceSelectionGroup)(self.wrapped.ExcitationSelection) if self.wrapped.ExcitationSelection else None

    @property
    def modal_analysis_options(self) -> '_4841.ModalAnalysisOptions':
        '''ModalAnalysisOptions: 'ModalAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4841.ModalAnalysisOptions)(self.wrapped.ModalAnalysisOptions) if self.wrapped.ModalAnalysisOptions else None

    @property
    def reference_speed_options(self) -> '_5434.SpeedOptionsForGearWhineAnalysisResults':
        '''SpeedOptionsForGearWhineAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5434.SpeedOptionsForGearWhineAnalysisResults)(self.wrapped.ReferenceSpeedOptions) if self.wrapped.ReferenceSpeedOptions else None

    @property
    def frequency_options(self) -> '_5383.FrequencyOptionsForGearWhineAnalysisResults':
        '''FrequencyOptionsForGearWhineAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5383.FrequencyOptionsForGearWhineAnalysisResults)(self.wrapped.FrequencyOptions) if self.wrapped.FrequencyOptions else None

    @property
    def per_mode_damping_factors(self) -> 'List[float]':
        '''List[float]: 'PerModeDampingFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PerModeDampingFactors, float)
        return value

    def set_per_mode_damping_factors(self, damping_values: 'List[float]'):
        ''' 'SetPerModeDampingFactors' is the original name of this method.

        Args:
            damping_values (List[float])
        '''

        damping_values = conversion.mp_to_pn_list_float(damping_values)
        self.wrapped.SetPerModeDampingFactors(damping_values)

    def set_per_mode_damping_factor(self, mode: 'int', damping: 'float'):
        ''' 'SetPerModeDampingFactor' is the original name of this method.

        Args:
            mode (int)
            damping (float)
        '''

        mode = int(mode)
        damping = float(damping)
        self.wrapped.SetPerModeDampingFactor(mode if mode else 0, damping if damping else 0.0)
