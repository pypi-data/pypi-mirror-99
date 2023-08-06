﻿'''_1912.py

ConicalGearOptimizationStrategyDatabase
'''


from mastapy.utility.databases import _1555
from mastapy.system_model.optimization import _1910
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_OPTIMIZATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'ConicalGearOptimizationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearOptimizationStrategyDatabase',)


class ConicalGearOptimizationStrategyDatabase(_1555.NamedDatabase['_1910.ConicalGearOptimisationStrategy']):
    '''ConicalGearOptimizationStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_OPTIMIZATION_STRATEGY_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearOptimizationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
