﻿'''_4002.py

CycloidalDiscCentralBearingConnectionParametricStudyTool
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2015
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3982
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CycloidalDiscCentralBearingConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionParametricStudyTool',)


class CycloidalDiscCentralBearingConnectionParametricStudyTool(_3982.CoaxialConnectionParametricStudyTool):
    '''CycloidalDiscCentralBearingConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2015.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2015.CycloidalDiscCentralBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
