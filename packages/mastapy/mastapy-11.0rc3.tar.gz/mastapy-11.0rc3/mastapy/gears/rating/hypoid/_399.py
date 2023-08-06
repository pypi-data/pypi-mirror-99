﻿'''_399.py

HypoidGearMeshRating
'''


from typing import List

from mastapy.gears.rating.iso_10300 import _386, _385
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.hypoid.standards import _404
from mastapy.gears.gear_designs.hypoid import _916
from mastapy.gears.rating.conical import _493
from mastapy.gears.rating.hypoid import _400
from mastapy.gears.rating.agma_gleason_conical import _513
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid', 'HypoidGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshRating',)


class HypoidGearMeshRating(_513.AGMAGleasonConicalGearMeshRating):
    '''HypoidGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b1(self) -> '_386.ISO10300MeshSingleFlankRatingMethodB1':
        '''ISO10300MeshSingleFlankRatingMethodB1: 'ISO10300HypoidMeshSingleFlankRatingMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_386.ISO10300MeshSingleFlankRatingMethodB1)(self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB1) if self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB1 else None

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b2(self) -> '_385.Iso10300MeshSingleFlankRatingHypoidMethodB2':
        '''Iso10300MeshSingleFlankRatingHypoidMethodB2: 'ISO10300HypoidMeshSingleFlankRatingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_385.Iso10300MeshSingleFlankRatingHypoidMethodB2)(self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB2) if self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB2 else None

    @property
    def gleason_hypoid_mesh_single_flank_rating(self) -> '_404.GleasonHypoidMeshSingleFlankRating':
        '''GleasonHypoidMeshSingleFlankRating: 'GleasonHypoidMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_404.GleasonHypoidMeshSingleFlankRating)(self.wrapped.GleasonHypoidMeshSingleFlankRating) if self.wrapped.GleasonHypoidMeshSingleFlankRating else None

    @property
    def hypoid_gear_mesh(self) -> '_916.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'HypoidGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_916.HypoidGearMeshDesign)(self.wrapped.HypoidGearMesh) if self.wrapped.HypoidGearMesh else None

    @property
    def meshed_gears(self) -> 'List[_493.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_493.ConicalMeshedGearRating))
        return value

    @property
    def gears_in_mesh(self) -> 'List[_493.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'GearsInMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsInMesh, constructor.new(_493.ConicalMeshedGearRating))
        return value

    @property
    def hypoid_gear_ratings(self) -> 'List[_400.HypoidGearRating]':
        '''List[HypoidGearRating]: 'HypoidGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearRatings, constructor.new(_400.HypoidGearRating))
        return value
