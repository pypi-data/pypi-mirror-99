﻿'''_5076.py

CVTBeltConnectionMultibodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1953
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5044
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CVTBeltConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionMultibodyDynamicsAnalysis',)


class CVTBeltConnectionMultibodyDynamicsAnalysis(_5044.BeltConnectionMultibodyDynamicsAnalysis):
    '''CVTBeltConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1953.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1953.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
