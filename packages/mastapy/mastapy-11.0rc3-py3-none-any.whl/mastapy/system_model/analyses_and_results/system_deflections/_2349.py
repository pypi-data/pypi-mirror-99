﻿'''_2349.py

MassDiscSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2062
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6218
from mastapy.system_model.analyses_and_results.power_flows import _3350
from mastapy.system_model.analyses_and_results.system_deflections import _2402
from mastapy._internal.python_net import python_net_import

_MASS_DISC_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'MassDiscSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscSystemDeflection',)


class MassDiscSystemDeflection(_2402.VirtualComponentSystemDeflection):
    '''MassDiscSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2062.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6218.MassDiscLoadCase':
        '''MassDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6218.MassDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3350.MassDiscPowerFlow':
        '''MassDiscPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3350.MassDiscPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def planetaries(self) -> 'List[MassDiscSystemDeflection]':
        '''List[MassDiscSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscSystemDeflection))
        return value
