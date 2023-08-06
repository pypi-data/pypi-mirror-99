﻿'''_4458.py

AbstractShaftModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _2083
from mastapy._internal import constructor
from mastapy.system_model.part_model.shaft_model import _2127
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.cycloidal import _2213
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4459
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'AbstractShaftModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftModalAnalysisAtASpeed',)


class AbstractShaftModalAnalysisAtASpeed(_4459.AbstractShaftOrHousingModalAnalysisAtASpeed):
    '''AbstractShaftModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2083.AbstractShaft':
        '''AbstractShaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.AbstractShaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_2127.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2127.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc(self) -> '_2213.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.CycloidalDisc.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
