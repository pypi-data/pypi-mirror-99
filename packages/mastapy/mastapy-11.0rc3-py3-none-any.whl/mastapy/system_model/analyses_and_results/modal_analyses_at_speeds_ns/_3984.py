﻿'''_3984.py

AbstractShaftOrHousingModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model import _1997, _2016
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2039
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4006
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'AbstractShaftOrHousingModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingModalAnalysesAtSpeeds',)


class AbstractShaftOrHousingModalAnalysesAtSpeeds(_4006.ComponentModalAnalysesAtSpeeds):
    '''AbstractShaftOrHousingModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1997.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.AbstractShaftOrHousing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_2016.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.ImportedFEComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2016.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_2039.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2039.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
