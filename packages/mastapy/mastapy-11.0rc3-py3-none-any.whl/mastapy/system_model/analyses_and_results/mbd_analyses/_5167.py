﻿'''_5167.py

TorqueConverterPumpMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2283
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6615
from mastapy.system_model.analyses_and_results.mbd_analyses import _5074
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterPumpMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpMultibodyDynamicsAnalysis',)


class TorqueConverterPumpMultibodyDynamicsAnalysis(_5074.CouplingHalfMultibodyDynamicsAnalysis):
    '''TorqueConverterPumpMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpMultibodyDynamicsAnalysis.TYPE'):
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
