﻿'''_314.py

ToothFlankFractureAnalysisContactPoint
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical.iso6336 import _315
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ToothFlankFractureAnalysisContactPoint')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothFlankFractureAnalysisContactPoint',)


class ToothFlankFractureAnalysisContactPoint(_0.APIBase):
    '''ToothFlankFractureAnalysisContactPoint

    This is a mastapy class.
    '''

    TYPE = _TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ToothFlankFractureAnalysisContactPoint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def effective_case_depth(self) -> 'float':
        '''float: 'EffectiveCaseDepth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EffectiveCaseDepth

    @property
    def maximum_residual_stress(self) -> 'float':
        '''float: 'MaximumResidualStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumResidualStress

    @property
    def hertzian_contact_stress(self) -> 'float':
        '''float: 'HertzianContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactStress

    @property
    def local_normal_radius_of_relative_curvature(self) -> 'float':
        '''float: 'LocalNormalRadiusOfRelativeCurvature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LocalNormalRadiusOfRelativeCurvature

    @property
    def half_of_hertzian_contact_width(self) -> 'float':
        '''float: 'HalfOfHertzianContactWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HalfOfHertzianContactWidth

    @property
    def transverse_thickness_at_the_diameter_corresponding_to_the_middle_between_b_and_d(self) -> 'float':
        '''float: 'TransverseThicknessAtTheDiameterCorrespondingToTheMiddleBetweenBAndD' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseThicknessAtTheDiameterCorrespondingToTheMiddleBetweenBAndD

    @property
    def material_factor(self) -> 'float':
        '''float: 'MaterialFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaterialFactor

    @property
    def material_factor_constant(self) -> 'float':
        '''float: 'MaterialFactorConstant' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaterialFactorConstant

    @property
    def maximum_material_exposure(self) -> 'float':
        '''float: 'MaximumMaterialExposure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumMaterialExposure

    @property
    def location(self) -> 'str':
        '''str: 'Location' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Location

    @property
    def analysis_point_with_maximum_local_material_exposure(self) -> '_315.ToothFlankFractureAnalysisPoint':
        '''ToothFlankFractureAnalysisPoint: 'AnalysisPointWithMaximumLocalMaterialExposure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_315.ToothFlankFractureAnalysisPoint)(self.wrapped.AnalysisPointWithMaximumLocalMaterialExposure) if self.wrapped.AnalysisPointWithMaximumLocalMaterialExposure else None

    @property
    def watch_points(self) -> 'List[_315.ToothFlankFractureAnalysisPoint]':
        '''List[ToothFlankFractureAnalysisPoint]: 'WatchPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WatchPoints, constructor.new(_315.ToothFlankFractureAnalysisPoint))
        return value
