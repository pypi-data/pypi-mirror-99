﻿'''_369.py

KlingelnbergCycloPalloidHypoidGearMeshRating
'''


from typing import List

from mastapy.gears.rating.klingelnberg_conical.kn3030 import _379
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.klingelnberg_hypoid import _908
from mastapy.gears.rating.klingelnberg_hypoid import _370
from mastapy.gears.rating.klingelnberg_conical import _372
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergHypoid', 'KlingelnbergCycloPalloidHypoidGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshRating',)


class KlingelnbergCycloPalloidHypoidGearMeshRating(_372.KlingelnbergCycloPalloidConicalGearMeshRating):
    '''KlingelnbergCycloPalloidHypoidGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def kn3030_pitting_and_bending_klingelnberg_mesh_single_flank_rating(self) -> '_379.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating':
        '''KlingelnbergCycloPalloidHypoidMeshSingleFlankRating: 'KN3030PittingAndBendingKlingelnbergMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_379.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating)(self.wrapped.KN3030PittingAndBendingKlingelnbergMeshSingleFlankRating) if self.wrapped.KN3030PittingAndBendingKlingelnbergMeshSingleFlankRating else None

    @property
    def kn3030_scuffing_klingelnberg_mesh_single_flank_rating(self) -> '_379.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating':
        '''KlingelnbergCycloPalloidHypoidMeshSingleFlankRating: 'KN3030ScuffingKlingelnbergMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_379.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating)(self.wrapped.KN3030ScuffingKlingelnbergMeshSingleFlankRating) if self.wrapped.KN3030ScuffingKlingelnbergMeshSingleFlankRating else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_908.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'KlingelnbergCycloPalloidHypoidGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_908.KlingelnbergCycloPalloidHypoidGearMeshDesign)(self.wrapped.KlingelnbergCycloPalloidHypoidGearMesh) if self.wrapped.KlingelnbergCycloPalloidHypoidGearMesh else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_ratings(self) -> 'List[_370.KlingelnbergCycloPalloidHypoidGearRating]':
        '''List[KlingelnbergCycloPalloidHypoidGearRating]: 'KlingelnbergCycloPalloidHypoidGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearRatings, constructor.new(_370.KlingelnbergCycloPalloidHypoidGearRating))
        return value
