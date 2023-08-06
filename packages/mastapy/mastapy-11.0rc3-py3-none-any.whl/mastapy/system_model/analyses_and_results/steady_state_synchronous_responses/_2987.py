﻿'''_2987.py

AbstractShaftOrHousingSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _2001, _2020
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2043
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3009
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'AbstractShaftOrHousingSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingSteadyStateSynchronousResponse',)


class AbstractShaftOrHousingSteadyStateSynchronousResponse(_3009.ComponentSteadyStateSynchronousResponse):
    '''AbstractShaftOrHousingSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2001.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2001.AbstractShaftOrHousing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_2020.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.ImportedFEComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2020.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_2043.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2043.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
