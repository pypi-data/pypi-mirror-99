﻿'''_154.py

AbstractGearSetRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears import _127
from mastapy.gears.rating import _153, _152
from mastapy.gears.analysis import _950
from mastapy._internal.python_net import python_net_import

_ABSTRACT_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'AbstractGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractGearSetRating',)


class AbstractGearSetRating(_950.AbstractGearSetAnalysis):
    '''AbstractGearSetRating

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def normalized_safety_factor_for_fatigue_and_static(self) -> 'float':
        '''float: 'NormalizedSafetyFactorForFatigueAndStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedSafetyFactorForFatigueAndStatic

    @property
    def normalized_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'NormalizedSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedSafetyFactorForFatigue

    @property
    def normalized_safety_factor_for_static(self) -> 'float':
        '''float: 'NormalizedSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedSafetyFactorForStatic

    @property
    def normalized_bending_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'NormalizedBendingSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedBendingSafetyFactorForFatigue

    @property
    def normalized_bending_safety_factor_for_static(self) -> 'float':
        '''float: 'NormalizedBendingSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedBendingSafetyFactorForStatic

    @property
    def normalized_contact_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'NormalizedContactSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedContactSafetyFactorForFatigue

    @property
    def normalized_contact_safety_factor_for_static(self) -> 'float':
        '''float: 'NormalizedContactSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedContactSafetyFactorForStatic

    @property
    def bending_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'BendingSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BendingSafetyFactorForFatigue

    @property
    def contact_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'ContactSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactSafetyFactorForFatigue

    @property
    def bending_safety_factor_for_static(self) -> 'float':
        '''float: 'BendingSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BendingSafetyFactorForStatic

    @property
    def contact_safety_factor_for_static(self) -> 'float':
        '''float: 'ContactSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactSafetyFactorForStatic

    @property
    def total_gear_reliability(self) -> 'float':
        '''float: 'TotalGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalGearReliability

    @property
    def transmission_properties_gears(self) -> '_127.GearSetDesignGroup':
        '''GearSetDesignGroup: 'TransmissionPropertiesGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_127.GearSetDesignGroup)(self.wrapped.TransmissionPropertiesGears) if self.wrapped.TransmissionPropertiesGears else None

    @property
    def gear_ratings(self) -> 'List[_153.AbstractGearRating]':
        '''List[AbstractGearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_153.AbstractGearRating))
        return value

    @property
    def gear_mesh_ratings(self) -> 'List[_152.AbstractGearMeshRating]':
        '''List[AbstractGearMeshRating]: 'GearMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshRatings, constructor.new(_152.AbstractGearMeshRating))
        return value
