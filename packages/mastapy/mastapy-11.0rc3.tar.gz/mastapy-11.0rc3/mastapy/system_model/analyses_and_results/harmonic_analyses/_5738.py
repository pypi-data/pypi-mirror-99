﻿'''_5738.py

TorqueConverterConnectionHarmonicAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _2032
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6613
from mastapy.system_model.analyses_and_results.system_deflections import _2494
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5632
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'TorqueConverterConnectionHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionHarmonicAnalysis',)


class TorqueConverterConnectionHarmonicAnalysis(_5632.CouplingConnectionHarmonicAnalysis):
    '''TorqueConverterConnectionHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2032.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6613.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6613.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2494.TorqueConverterConnectionSystemDeflection':
        '''TorqueConverterConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2494.TorqueConverterConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
