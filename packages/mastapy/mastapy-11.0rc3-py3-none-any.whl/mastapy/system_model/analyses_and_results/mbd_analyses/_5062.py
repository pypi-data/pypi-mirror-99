﻿'''_5062.py

ConceptCouplingConnectionMultibodyDynamicsAnalysis
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.couplings import _2024
from mastapy.system_model.analyses_and_results.static_loads import _6473
from mastapy.system_model.analyses_and_results.mbd_analyses import _5073
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ConceptCouplingConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionMultibodyDynamicsAnalysis',)


class ConceptCouplingConnectionMultibodyDynamicsAnalysis(_5073.CouplingConnectionMultibodyDynamicsAnalysis):
    '''ConceptCouplingConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def specified_torque_ratio(self) -> 'float':
        '''float: 'SpecifiedTorqueRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpecifiedTorqueRatio

    @property
    def specified_speed_ratio(self) -> 'float':
        '''float: 'SpecifiedSpeedRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpecifiedSpeedRatio

    @property
    def connection_design(self) -> '_2024.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2024.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6473.ConceptCouplingConnectionLoadCase':
        '''ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6473.ConceptCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
