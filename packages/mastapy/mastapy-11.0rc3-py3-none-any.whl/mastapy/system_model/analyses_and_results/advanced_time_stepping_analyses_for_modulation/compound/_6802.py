﻿'''_6802.py

ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2022
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6672
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6818
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation',)


class ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation(_6818.CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2022.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2022.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_6672.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ClutchConnectionAdvancedTimeSteppingAnalysisForModulation]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_6672.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_6672.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ClutchConnectionAdvancedTimeSteppingAnalysisForModulation]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_6672.ClutchConnectionAdvancedTimeSteppingAnalysisForModulation))
        return value
