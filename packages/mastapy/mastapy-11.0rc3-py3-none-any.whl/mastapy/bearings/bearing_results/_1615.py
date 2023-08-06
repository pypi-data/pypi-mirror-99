﻿'''_1615.py

LoadedRollingBearingDutyCycle
'''


from mastapy._internal import constructor
from mastapy.utility.property import (
    _1371, _1370, _1368, _1369
)
from mastapy.bearings import _1541
from mastapy.bearings.bearing_results.rolling import _1711
from mastapy.bearings.bearing_results import _1612
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLING_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedRollingBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedRollingBearingDutyCycle',)


class LoadedRollingBearingDutyCycle(_1612.LoadedNonLinearBearingDutyCycleResults):
    '''LoadedRollingBearingDutyCycle

    This is a mastapy class.
    '''

    TYPE = _LOADED_ROLLING_BEARING_DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedRollingBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_lubricating_film_thickness(self) -> 'float':
        '''float: 'MinimumLubricatingFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLubricatingFilmThickness

    @property
    def minimum_lubricating_film_thickness_inner(self) -> 'float':
        '''float: 'MinimumLubricatingFilmThicknessInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLubricatingFilmThicknessInner

    @property
    def minimum_lambda_ratio(self) -> 'float':
        '''float: 'MinimumLambdaRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLambdaRatio

    @property
    def lambda_ratio_outer(self) -> 'float':
        '''float: 'LambdaRatioOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LambdaRatioOuter

    @property
    def lambda_ratio_inner(self) -> 'float':
        '''float: 'LambdaRatioInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LambdaRatioInner

    @property
    def minimum_lubricating_film_thickness_outer(self) -> 'float':
        '''float: 'MinimumLubricatingFilmThicknessOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLubricatingFilmThicknessOuter

    @property
    def iso2812007_basic_rating_life_time(self) -> 'float':
        '''float: 'ISO2812007BasicRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007BasicRatingLifeTime

    @property
    def iso2812007_basic_rating_life_reliability(self) -> 'float':
        '''float: 'ISO2812007BasicRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007BasicRatingLifeReliability

    @property
    def iso2812007_basic_rating_life_unreliability(self) -> 'float':
        '''float: 'ISO2812007BasicRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007BasicRatingLifeUnreliability

    @property
    def iso2812007_modified_rating_life_reliability(self) -> 'float':
        '''float: 'ISO2812007ModifiedRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007ModifiedRatingLifeReliability

    @property
    def iso2812007_modified_rating_life_unreliability(self) -> 'float':
        '''float: 'ISO2812007ModifiedRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007ModifiedRatingLifeUnreliability

    @property
    def isots162812008_basic_reference_rating_life_reliability(self) -> 'float':
        '''float: 'ISOTS162812008BasicReferenceRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008BasicReferenceRatingLifeReliability

    @property
    def isots162812008_basic_reference_rating_life_unreliability(self) -> 'float':
        '''float: 'ISOTS162812008BasicReferenceRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008BasicReferenceRatingLifeUnreliability

    @property
    def isots162812008_modified_reference_rating_life_reliability(self) -> 'float':
        '''float: 'ISOTS162812008ModifiedReferenceRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeReliability

    @property
    def isots162812008_modified_reference_rating_life_unreliability(self) -> 'float':
        '''float: 'ISOTS162812008ModifiedReferenceRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeUnreliability

    @property
    def skf_bearing_rating_life_reliability(self) -> 'float':
        '''float: 'SKFBearingRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SKFBearingRatingLifeReliability

    @property
    def skf_bearing_rating_life_unreliability(self) -> 'float':
        '''float: 'SKFBearingRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SKFBearingRatingLifeUnreliability

    @property
    def iso2812007_modified_rating_life_time(self) -> 'float':
        '''float: 'ISO2812007ModifiedRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007ModifiedRatingLifeTime

    @property
    def isots162812008_basic_reference_rating_life_time(self) -> 'float':
        '''float: 'ISOTS162812008BasicReferenceRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008BasicReferenceRatingLifeTime

    @property
    def isots162812008_modified_reference_rating_life_time(self) -> 'float':
        '''float: 'ISOTS162812008ModifiedReferenceRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeTime

    @property
    def skf_bearing_rating_life_time(self) -> 'float':
        '''float: 'SKFBearingRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SKFBearingRatingLifeTime

    @property
    def iso2812007_basic_rating_life_damage(self) -> 'float':
        '''float: 'ISO2812007BasicRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007BasicRatingLifeDamage

    @property
    def iso2812007_modified_rating_life_damage(self) -> 'float':
        '''float: 'ISO2812007ModifiedRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007ModifiedRatingLifeDamage

    @property
    def isots162812008_modified_reference_rating_life_damage(self) -> 'float':
        '''float: 'ISOTS162812008ModifiedReferenceRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeDamage

    @property
    def isots162812008_basic_reference_rating_life_damage(self) -> 'float':
        '''float: 'ISOTS162812008BasicReferenceRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008BasicReferenceRatingLifeDamage

    @property
    def skf_bearing_rating_life_damage(self) -> 'float':
        '''float: 'SKFBearingRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SKFBearingRatingLifeDamage

    @property
    def maximum_element_normal_stress(self) -> 'float':
        '''float: 'MaximumElementNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumElementNormalStress

    @property
    def iso762006_recommended_maximum_element_normal_stress(self) -> 'float':
        '''float: 'ISO762006RecommendedMaximumElementNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO762006RecommendedMaximumElementNormalStress

    @property
    def iso2812007_dynamic_equivalent_load(self) -> 'float':
        '''float: 'ISO2812007DynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007DynamicEquivalentLoad

    @property
    def isots162812008_dynamic_equivalent_load(self) -> 'float':
        '''float: 'ISOTS162812008DynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008DynamicEquivalentLoad

    @property
    def iso2812007_basic_rating_life_safety_factor(self) -> 'float':
        '''float: 'ISO2812007BasicRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007BasicRatingLifeSafetyFactor

    @property
    def iso2812007_modified_rating_life_safety_factor(self) -> 'float':
        '''float: 'ISO2812007ModifiedRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007ModifiedRatingLifeSafetyFactor

    @property
    def isots162812008_basic_reference_rating_life_safety_factor(self) -> 'float':
        '''float: 'ISOTS162812008BasicReferenceRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008BasicReferenceRatingLifeSafetyFactor

    @property
    def isots162812008_modified_reference_rating_life_safety_factor(self) -> 'float':
        '''float: 'ISOTS162812008ModifiedReferenceRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISOTS162812008ModifiedReferenceRatingLifeSafetyFactor

    @property
    def worst_iso762006_safety_factor_static_equivalent_load_capacity_ratio(self) -> 'float':
        '''float: 'WorstISO762006SafetyFactorStaticEquivalentLoadCapacityRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorstISO762006SafetyFactorStaticEquivalentLoadCapacityRatio

    @property
    def static_equivalent_load_capacity_ratio_limit(self) -> 'float':
        '''float: 'StaticEquivalentLoadCapacityRatioLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticEquivalentLoadCapacityRatioLimit

    @property
    def maximum_element_normal_stress_inner_summary(self) -> '_1371.DutyCyclePropertySummaryStress[_1541.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryStress[BearingLoadCaseResultsLightweight]: 'MaximumElementNormalStressInnerSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1371.DutyCyclePropertySummaryStress)[_1541.BearingLoadCaseResultsLightweight](self.wrapped.MaximumElementNormalStressInnerSummary) if self.wrapped.MaximumElementNormalStressInnerSummary else None

    @property
    def maximum_element_normal_stress_outer_summary(self) -> '_1371.DutyCyclePropertySummaryStress[_1541.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryStress[BearingLoadCaseResultsLightweight]: 'MaximumElementNormalStressOuterSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1371.DutyCyclePropertySummaryStress)[_1541.BearingLoadCaseResultsLightweight](self.wrapped.MaximumElementNormalStressOuterSummary) if self.wrapped.MaximumElementNormalStressOuterSummary else None

    @property
    def maximum_element_normal_stress_summary(self) -> '_1371.DutyCyclePropertySummaryStress[_1541.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryStress[BearingLoadCaseResultsLightweight]: 'MaximumElementNormalStressSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1371.DutyCyclePropertySummaryStress)[_1541.BearingLoadCaseResultsLightweight](self.wrapped.MaximumElementNormalStressSummary) if self.wrapped.MaximumElementNormalStressSummary else None

    @property
    def misalignment_summary(self) -> '_1370.DutyCyclePropertySummarySmallAngle[_1541.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummarySmallAngle[BearingLoadCaseResultsLightweight]: 'MisalignmentSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1370.DutyCyclePropertySummarySmallAngle)[_1541.BearingLoadCaseResultsLightweight](self.wrapped.MisalignmentSummary) if self.wrapped.MisalignmentSummary else None

    @property
    def iso2812007_dynamic_equivalent_load_summary(self) -> '_1368.DutyCyclePropertySummaryForce[_1541.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ISO2812007DynamicEquivalentLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1368.DutyCyclePropertySummaryForce)[_1541.BearingLoadCaseResultsLightweight](self.wrapped.ISO2812007DynamicEquivalentLoadSummary) if self.wrapped.ISO2812007DynamicEquivalentLoadSummary else None

    @property
    def isots162812008_dynamic_equivalent_load_summary(self) -> '_1368.DutyCyclePropertySummaryForce[_1541.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ISOTS162812008DynamicEquivalentLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1368.DutyCyclePropertySummaryForce)[_1541.BearingLoadCaseResultsLightweight](self.wrapped.ISOTS162812008DynamicEquivalentLoadSummary) if self.wrapped.ISOTS162812008DynamicEquivalentLoadSummary else None

    @property
    def maximum_truncation_summary(self) -> '_1369.DutyCyclePropertySummaryPercentage[_1541.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryPercentage[BearingLoadCaseResultsLightweight]: 'MaximumTruncationSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1369.DutyCyclePropertySummaryPercentage)[_1541.BearingLoadCaseResultsLightweight](self.wrapped.MaximumTruncationSummary) if self.wrapped.MaximumTruncationSummary else None

    @property
    def maximum_static_contact_stress_duty_cycle(self) -> '_1711.MaximumStaticContactStressDutyCycle':
        '''MaximumStaticContactStressDutyCycle: 'MaximumStaticContactStressDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1711.MaximumStaticContactStressDutyCycle)(self.wrapped.MaximumStaticContactStressDutyCycle) if self.wrapped.MaximumStaticContactStressDutyCycle else None
