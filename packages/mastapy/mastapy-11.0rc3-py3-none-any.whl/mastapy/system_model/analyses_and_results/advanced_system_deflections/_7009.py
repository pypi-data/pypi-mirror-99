﻿'''_7009.py

RootAssemblyAdvancedSystemDeflection
'''


from mastapy.system_model.part_model import _2151
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6913, _6919
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'RootAssemblyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyAdvancedSystemDeflection',)


class RootAssemblyAdvancedSystemDeflection(_6919.AssemblyAdvancedSystemDeflection):
    '''RootAssemblyAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2151.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2151.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def advanced_system_deflection_inputs(self) -> '_6913.AdvancedSystemDeflection':
        '''AdvancedSystemDeflection: 'AdvancedSystemDeflectionInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6913.AdvancedSystemDeflection)(self.wrapped.AdvancedSystemDeflectionInputs) if self.wrapped.AdvancedSystemDeflectionInputs else None
