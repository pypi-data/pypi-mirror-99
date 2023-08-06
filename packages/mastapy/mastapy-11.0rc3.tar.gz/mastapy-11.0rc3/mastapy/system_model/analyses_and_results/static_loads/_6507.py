﻿'''_6507.py

ElectricMachineDetailDatabase
'''


from mastapy.utility.databases import _1555
from mastapy.system_model.analyses_and_results.static_loads import _6506
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_DETAIL_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineDetailDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineDetailDatabase',)


class ElectricMachineDetailDatabase(_1555.NamedDatabase['_6506.ElectricMachineDetail']):
    '''ElectricMachineDetailDatabase

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_DETAIL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineDetailDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
