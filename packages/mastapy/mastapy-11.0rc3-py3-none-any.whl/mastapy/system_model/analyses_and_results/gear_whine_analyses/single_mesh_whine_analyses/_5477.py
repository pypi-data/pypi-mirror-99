﻿'''_5477.py

ClutchConnectionSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _1934
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6117
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5493
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ClutchConnectionSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionSingleMeshWhineAnalysis',)


class ClutchConnectionSingleMeshWhineAnalysis(_5493.CouplingConnectionSingleMeshWhineAnalysis):
    '''ClutchConnectionSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1934.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1934.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6117.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6117.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
