﻿'''_851.py

MicroGeometryDesignSpaceSearchChartInformation
'''


from mastapy.gears.gear_set_pareto_optimiser import (
    _849, _852, _837, _850
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.ltca.cylindrical import _796
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CHART_INFORMATION = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'MicroGeometryDesignSpaceSearchChartInformation')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryDesignSpaceSearchChartInformation',)


class MicroGeometryDesignSpaceSearchChartInformation(_837.ChartInfoBase['_796.CylindricalGearSetLoadDistributionAnalysis', '_850.MicroGeometryDesignSpaceSearchCandidate']):
    '''MicroGeometryDesignSpaceSearchChartInformation

    This is a mastapy class.
    '''

    TYPE = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CHART_INFORMATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryDesignSpaceSearchChartInformation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def optimiser(self) -> '_849.MicroGeometryDesignSpaceSearch':
        '''MicroGeometryDesignSpaceSearch: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _849.MicroGeometryDesignSpaceSearch.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to MicroGeometryDesignSpaceSearch. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None

    @property
    def optimiser_of_type_micro_geometry_gear_set_design_space_search(self) -> '_852.MicroGeometryGearSetDesignSpaceSearch':
        '''MicroGeometryGearSetDesignSpaceSearch: 'Optimiser' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _852.MicroGeometryGearSetDesignSpaceSearch.TYPE not in self.wrapped.Optimiser.__class__.__mro__:
            raise CastException('Failed to cast optimiser to MicroGeometryGearSetDesignSpaceSearch. Expected: {}.'.format(self.wrapped.Optimiser.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Optimiser.__class__)(self.wrapped.Optimiser) if self.wrapped.Optimiser else None
