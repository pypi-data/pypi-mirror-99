﻿'''_6419.py

TorqueConverterPumpAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2202
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6271
from mastapy.system_model.analyses_and_results.system_deflections import _2396
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6343
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'TorqueConverterPumpAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpAdvancedSystemDeflection',)


class TorqueConverterPumpAdvancedSystemDeflection(_6343.CouplingHalfAdvancedSystemDeflection):
    '''TorqueConverterPumpAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2202.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2202.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6271.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6271.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2396.TorqueConverterPumpSystemDeflection]':
        '''List[TorqueConverterPumpSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2396.TorqueConverterPumpSystemDeflection))
        return value
