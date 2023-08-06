﻿'''_6253.py

SpringDamperLoadCase
'''


from mastapy.system_model.part_model.couplings import _2194
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6157
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpringDamperLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperLoadCase',)


class SpringDamperLoadCase(_6157.CouplingLoadCase):
    '''SpringDamperLoadCase

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2194.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
