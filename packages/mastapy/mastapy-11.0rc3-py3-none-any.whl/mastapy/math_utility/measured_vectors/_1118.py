﻿'''_1118.py

ForceAndDisplacementResults
'''


from mastapy.math_utility.measured_vectors import _1123, _1117
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_FORCE_AND_DISPLACEMENT_RESULTS = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'ForceAndDisplacementResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ForceAndDisplacementResults',)


class ForceAndDisplacementResults(_1117.AbstractForceAndDisplacementResults):
    '''ForceAndDisplacementResults

    This is a mastapy class.
    '''

    TYPE = _FORCE_AND_DISPLACEMENT_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ForceAndDisplacementResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def displacement(self) -> '_1123.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'Displacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1123.VectorWithLinearAndAngularComponents)(self.wrapped.Displacement) if self.wrapped.Displacement else None
