﻿'''_4842.py

PlanetCarrierModalAnalysis
'''


from mastapy.system_model.part_model import _2146
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6573
from mastapy.system_model.analyses_and_results.system_deflections import _2456
from mastapy.system_model.analyses_and_results.modal_analyses import _4833
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PlanetCarrierModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierModalAnalysis',)


class PlanetCarrierModalAnalysis(_4833.MountableComponentModalAnalysis):
    '''PlanetCarrierModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2146.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2146.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6573.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6573.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2456.PlanetCarrierSystemDeflection':
        '''PlanetCarrierSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2456.PlanetCarrierSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
