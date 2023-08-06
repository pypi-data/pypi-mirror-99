﻿'''_2028.py

Bolt
'''


from mastapy.bolts import _1057
from mastapy._internal import constructor
from mastapy.system_model.part_model import _2029, _2030
from mastapy._internal.python_net import python_net_import

_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')


__docformat__ = 'restructuredtext en'
__all__ = ('Bolt',)


class Bolt(_2030.Component):
    '''Bolt

    This is a mastapy class.
    '''

    TYPE = _BOLT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Bolt.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bolt(self) -> '_1057.LoadedBolt':
        '''LoadedBolt: 'LoadedBolt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1057.LoadedBolt)(self.wrapped.LoadedBolt) if self.wrapped.LoadedBolt else None

    @property
    def bolted_joint(self) -> '_2029.BoltedJoint':
        '''BoltedJoint: 'BoltedJoint' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2029.BoltedJoint)(self.wrapped.BoltedJoint) if self.wrapped.BoltedJoint else None
