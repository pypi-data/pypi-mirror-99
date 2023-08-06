﻿'''_2149.py

WormGear
'''


from mastapy.gears.gear_designs.worm import _722, _721, _725
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.gears import _2128
from mastapy._internal.python_net import python_net_import

_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGear',)


class WormGear(_2128.Gear):
    '''WormGear

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_design(self) -> '_722.WormGearDesign':
        '''WormGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _722.WormGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to WormGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearDesign.__class__)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def worm_gear_design(self) -> '_722.WormGearDesign':
        '''WormGearDesign: 'WormGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _722.WormGearDesign.TYPE not in self.wrapped.WormGearDesign.__class__.__mro__:
            raise CastException('Failed to cast worm_gear_design to WormGearDesign. Expected: {}.'.format(self.wrapped.WormGearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WormGearDesign.__class__)(self.wrapped.WormGearDesign) if self.wrapped.WormGearDesign else None
