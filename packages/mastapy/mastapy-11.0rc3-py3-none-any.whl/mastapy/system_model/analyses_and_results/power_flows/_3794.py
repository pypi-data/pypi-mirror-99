﻿'''_3794.py

ShaftHubConnectionPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2273
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6587
from mastapy.detailed_rigid_connectors.rating import _1200
from mastapy.detailed_rigid_connectors.splines.ratings import (
    _1188, _1190, _1192, _1194,
    _1196
)
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.keyed_joints.rating import _1206
from mastapy.detailed_rigid_connectors.interference_fits.rating import _1213
from mastapy.system_model.analyses_and_results.power_flows import _3732
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ShaftHubConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionPowerFlow',)


class ShaftHubConnectionPowerFlow(_3732.ConnectorPowerFlow):
    '''ShaftHubConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2273.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6587.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6587.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_1200.ShaftHubConnectionRating':
        '''ShaftHubConnectionRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1200.ShaftHubConnectionRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to ShaftHubConnectionRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_agma6123_spline_joint_rating(self) -> '_1188.AGMA6123SplineJointRating':
        '''AGMA6123SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1188.AGMA6123SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to AGMA6123SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_din5466_spline_rating(self) -> '_1190.DIN5466SplineRating':
        '''DIN5466SplineRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1190.DIN5466SplineRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to DIN5466SplineRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_gbt17855_spline_joint_rating(self) -> '_1192.GBT17855SplineJointRating':
        '''GBT17855SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1192.GBT17855SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to GBT17855SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_sae_spline_joint_rating(self) -> '_1194.SAESplineJointRating':
        '''SAESplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1194.SAESplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SAESplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spline_joint_rating(self) -> '_1196.SplineJointRating':
        '''SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1196.SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_keyway_rating(self) -> '_1206.KeywayRating':
        '''KeywayRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1206.KeywayRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to KeywayRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_interference_fit_rating(self) -> '_1213.InterferenceFitRating':
        '''InterferenceFitRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1213.InterferenceFitRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to InterferenceFitRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
