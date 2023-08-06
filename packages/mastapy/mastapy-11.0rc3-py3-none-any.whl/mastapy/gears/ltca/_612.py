﻿'''_612.py

GearContactStiffnessNode
'''


from mastapy.gears.ltca import _620
from mastapy._internal.python_net import python_net_import

_GEAR_CONTACT_STIFFNESS_NODE = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearContactStiffnessNode')


__docformat__ = 'restructuredtext en'
__all__ = ('GearContactStiffnessNode',)


class GearContactStiffnessNode(_620.GearStiffnessNode):
    '''GearContactStiffnessNode

    This is a mastapy class.
    '''

    TYPE = _GEAR_CONTACT_STIFFNESS_NODE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearContactStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
