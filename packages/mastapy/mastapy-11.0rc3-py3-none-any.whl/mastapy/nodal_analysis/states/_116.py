﻿'''_116.py

NodeVectorState
'''


from mastapy.nodal_analysis.states import _114
from mastapy._internal.python_net import python_net_import

_NODE_VECTOR_STATE = python_net_import('SMT.MastaAPI.NodalAnalysis.States', 'NodeVectorState')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeVectorState',)


class NodeVectorState(_114.EntityVectorState):
    '''NodeVectorState

    This is a mastapy class.
    '''

    TYPE = _NODE_VECTOR_STATE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodeVectorState.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
