﻿'''_3814.py

SynchroniserPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2277
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6608
from mastapy.system_model.analyses_and_results.power_flows import _3812, _3797
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SynchroniserPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserPowerFlow',)


class SynchroniserPowerFlow(_3797.SpecialisedAssemblyPowerFlow):
    '''SynchroniserPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2277.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6608.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6608.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cones(self) -> 'List[_3812.SynchroniserHalfPowerFlow]':
        '''List[SynchroniserHalfPowerFlow]: 'Cones' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Cones, constructor.new(_3812.SynchroniserHalfPowerFlow))
        return value
