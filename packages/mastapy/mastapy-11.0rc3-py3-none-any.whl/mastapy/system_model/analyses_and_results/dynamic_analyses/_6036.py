﻿'''_6036.py

TorqueConverterPumpDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2283
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6615
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5955
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'TorqueConverterPumpDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpDynamicAnalysis',)


class TorqueConverterPumpDynamicAnalysis(_5955.CouplingHalfDynamicAnalysis):
    '''TorqueConverterPumpDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2283.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2283.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6615.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6615.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
