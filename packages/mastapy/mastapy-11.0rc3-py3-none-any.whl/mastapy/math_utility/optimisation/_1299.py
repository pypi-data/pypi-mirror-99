﻿'''_1299.py

DesignSpaceSearchStrategyDatabase
'''


from mastapy.utility.databases import _1549
from mastapy.math_utility.optimisation import _1309
from mastapy._internal.python_net import python_net_import

_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'DesignSpaceSearchStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignSpaceSearchStrategyDatabase',)


class DesignSpaceSearchStrategyDatabase(_1549.NamedDatabase['_1309.ParetoOptimisationStrategy']):
    '''DesignSpaceSearchStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _DESIGN_SPACE_SEARCH_STRATEGY_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignSpaceSearchStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
