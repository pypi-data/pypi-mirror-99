﻿'''_1961.py

TorqueConverterPumpSocket
'''


from mastapy.system_model.connections_and_sockets.couplings import _1955
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterPumpSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpSocket',)


class TorqueConverterPumpSocket(_1955.CouplingSocket):
    '''TorqueConverterPumpSocket

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
