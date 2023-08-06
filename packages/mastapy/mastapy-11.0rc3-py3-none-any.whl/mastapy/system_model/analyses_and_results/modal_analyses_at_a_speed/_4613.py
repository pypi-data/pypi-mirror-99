﻿'''_4613.py

TorqueConverterTurbineModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2285
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6616
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4531
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'TorqueConverterTurbineModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineModalAnalysisAtASpeed',)


class TorqueConverterTurbineModalAnalysisAtASpeed(_4531.CouplingHalfModalAnalysisAtASpeed):
    '''TorqueConverterTurbineModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2285.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2285.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6616.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6616.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
