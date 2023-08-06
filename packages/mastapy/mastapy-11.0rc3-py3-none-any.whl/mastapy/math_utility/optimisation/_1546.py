﻿'''_1546.py

ParetoOptimisationInput
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility import _1489
from mastapy.math_utility.measured_ranges import _1564
from mastapy._internal.cast_exception import CastException
from mastapy.math_utility.optimisation import _1556, _1553
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_INPUT = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationInput')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationInput',)


class ParetoOptimisationInput(_1553.ParetoOptimistaionVariable):
    '''ParetoOptimisationInput

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_INPUT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationInput.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_steps(self) -> 'int':
        '''int: 'NumberOfSteps' is the original name of this property.'''

        return self.wrapped.NumberOfSteps

    @number_of_steps.setter
    def number_of_steps(self, value: 'int'):
        self.wrapped.NumberOfSteps = int(value) if value else 0

    @property
    def range(self) -> '_1489.Range':
        '''Range: 'Range' is the original name of this property.'''

        if _1489.Range.TYPE not in self.wrapped.Range.__class__.__mro__:
            raise CastException('Failed to cast range to Range. Expected: {}.'.format(self.wrapped.Range.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Range.__class__)(self.wrapped.Range) if self.wrapped.Range else None

    @range.setter
    def range(self, value: '_1489.Range'):
        value = value.wrapped if value else None
        self.wrapped.Range = value

    @property
    def specify_input_range_as(self) -> '_1556.SpecifyOptimisationInputAs':
        '''SpecifyOptimisationInputAs: 'SpecifyInputRangeAs' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SpecifyInputRangeAs)
        return constructor.new(_1556.SpecifyOptimisationInputAs)(value) if value else None

    @specify_input_range_as.setter
    def specify_input_range_as(self, value: '_1556.SpecifyOptimisationInputAs'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpecifyInputRangeAs = value
