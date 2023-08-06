﻿'''_125.py

BarMBD
'''


from mastapy.nodal_analysis.nodal_entities import _129
from mastapy._internal.python_net import python_net_import

_BAR_MBD = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'BarMBD')


__docformat__ = 'restructuredtext en'
__all__ = ('BarMBD',)


class BarMBD(_129.ComponentNodalComposite):
    '''BarMBD

    This is a mastapy class.
    '''

    TYPE = _BAR_MBD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BarMBD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
