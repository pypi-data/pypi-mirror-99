﻿'''_1942.py

SpringDamperConnection
'''


from mastapy.system_model import _1833
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.nodal_analysis import _1396
from mastapy.system_model.connections_and_sockets.couplings import _1938
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnection',)


class SpringDamperConnection(_1938.CouplingConnection):
    '''SpringDamperConnection

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def damping_option(self) -> '_1833.ComponentDampingOption':
        '''ComponentDampingOption: 'DampingOption' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.DampingOption)
        return constructor.new(_1833.ComponentDampingOption)(value) if value else None

    @damping_option.setter
    def damping_option(self, value: '_1833.ComponentDampingOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DampingOption = value

    @property
    def damping(self) -> '_1396.LinearDampingConnectionProperties':
        '''LinearDampingConnectionProperties: 'Damping' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1396.LinearDampingConnectionProperties)(self.wrapped.Damping) if self.wrapped.Damping else None
