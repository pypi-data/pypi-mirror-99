﻿'''_494.py

ConicalMeshSingleFlankRating
'''


from mastapy.gears.rating import _327
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalMeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshSingleFlankRating',)


class ConicalMeshSingleFlankRating(_327.MeshSingleFlankRating):
    '''ConicalMeshSingleFlankRating

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_SINGLE_FLANK_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
