﻿'''_6346.py

CVTPulleyAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2181
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6390
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CVTPulleyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyAdvancedSystemDeflection',)


class CVTPulleyAdvancedSystemDeflection(_6390.PulleyAdvancedSystemDeflection):
    '''CVTPulleyAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
