﻿'''_2043.py

ConcentricOrParallelPartGroup
'''


from mastapy.system_model.part_model.part_groups import _2048
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_OR_PARALLEL_PART_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'ConcentricOrParallelPartGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricOrParallelPartGroup',)


class ConcentricOrParallelPartGroup(_2048.PartGroup):
    '''ConcentricOrParallelPartGroup

    This is a mastapy class.
    '''

    TYPE = _CONCENTRIC_OR_PARALLEL_PART_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConcentricOrParallelPartGroup.TYPE'):
        super().__init__(instance_to_wrap)
