﻿'''_1652.py

LoadedBallBearingRow
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import (
    _1651, _1632, _1635, _1661,
    _1666, _1685, _1701, _1704,
    _1650, _1683
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingRow',)


class LoadedBallBearingRow(_1683.LoadedRollingBearingRow):
    '''LoadedBallBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_BALL_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBallBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def dynamic_equivalent_load_inner(self) -> 'float':
        '''float: 'DynamicEquivalentLoadInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicEquivalentLoadInner

    @property
    def dynamic_equivalent_load_outer(self) -> 'float':
        '''float: 'DynamicEquivalentLoadOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicEquivalentLoadOuter

    @property
    def axial_ball_movement(self) -> 'float':
        '''float: 'AxialBallMovement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialBallMovement

    @property
    def hertzian_semi_minor_dimension_highest_load_inner(self) -> 'float':
        '''float: 'HertzianSemiMinorDimensionHighestLoadInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianSemiMinorDimensionHighestLoadInner

    @property
    def hertzian_semi_minor_dimension_highest_load_outer(self) -> 'float':
        '''float: 'HertzianSemiMinorDimensionHighestLoadOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianSemiMinorDimensionHighestLoadOuter

    @property
    def hertzian_semi_major_dimension_highest_load_inner(self) -> 'float':
        '''float: 'HertzianSemiMajorDimensionHighestLoadInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianSemiMajorDimensionHighestLoadInner

    @property
    def hertzian_semi_major_dimension_highest_load_outer(self) -> 'float':
        '''float: 'HertzianSemiMajorDimensionHighestLoadOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianSemiMajorDimensionHighestLoadOuter

    @property
    def track_truncation_occurring_beyond_permissible_limit(self) -> 'bool':
        '''bool: 'TrackTruncationOccurringBeyondPermissibleLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TrackTruncationOccurringBeyondPermissibleLimit

    @property
    def truncation_warning(self) -> 'str':
        '''str: 'TruncationWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TruncationWarning

    @property
    def worst_hertzian_ellipse_major_2b_track_truncation(self) -> 'float':
        '''float: 'WorstHertzianEllipseMajor2bTrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorstHertzianEllipseMajor2bTrackTruncation

    @property
    def smallest_arc_distance_of_raceway_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'SmallestArcDistanceOfRacewayEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestArcDistanceOfRacewayEdgeToHertzianContact

    @property
    def element_with_worst_track_truncation(self) -> 'str':
        '''str: 'ElementWithWorstTrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElementWithWorstTrackTruncation

    @property
    def loaded_bearing(self) -> '_1651.LoadedBallBearingResults':
        '''LoadedBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1651.LoadedBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_angular_contact_ball_bearing_results(self) -> '_1632.LoadedAngularContactBallBearingResults':
        '''LoadedAngularContactBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1632.LoadedAngularContactBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAngularContactBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_angular_contact_thrust_ball_bearing_results(self) -> '_1635.LoadedAngularContactThrustBallBearingResults':
        '''LoadedAngularContactThrustBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1635.LoadedAngularContactThrustBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAngularContactThrustBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_deep_groove_ball_bearing_results(self) -> '_1661.LoadedDeepGrooveBallBearingResults':
        '''LoadedDeepGrooveBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1661.LoadedDeepGrooveBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedDeepGrooveBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_four_point_contact_ball_bearing_results(self) -> '_1666.LoadedFourPointContactBallBearingResults':
        '''LoadedFourPointContactBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1666.LoadedFourPointContactBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedFourPointContactBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_self_aligning_ball_bearing_results(self) -> '_1685.LoadedSelfAligningBallBearingResults':
        '''LoadedSelfAligningBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1685.LoadedSelfAligningBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedSelfAligningBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_three_point_contact_ball_bearing_results(self) -> '_1701.LoadedThreePointContactBallBearingResults':
        '''LoadedThreePointContactBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1701.LoadedThreePointContactBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedThreePointContactBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_thrust_ball_bearing_results(self) -> '_1704.LoadedThrustBallBearingResults':
        '''LoadedThrustBallBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1704.LoadedThrustBallBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedThrustBallBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def race_results(self) -> 'List[_1650.LoadedBallBearingRaceResults]':
        '''List[LoadedBallBearingRaceResults]: 'RaceResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RaceResults, constructor.new(_1650.LoadedBallBearingRaceResults))
        return value
