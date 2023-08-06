﻿'''_1439.py

GearMeshNodePair
'''


from mastapy.nodal_analysis.nodal_entities import _1427
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_NODE_PAIR = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'GearMeshNodePair')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshNodePair',)


class GearMeshNodePair(_1427.ArbitraryNodalComponent):
    '''GearMeshNodePair

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_NODE_PAIR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshNodePair.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
