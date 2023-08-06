﻿'''_5267.py

AbstractAssemblyStaticLoadCaseGroup
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5272
from mastapy.system_model.part_model import _2000
from mastapy.system_model.analyses_and_results.static_loads import _6070
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'AbstractAssemblyStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyStaticLoadCaseGroup',)


TAssembly = TypeVar('TAssembly', bound='_2000.AbstractAssembly')
TAssemblyStaticLoad = TypeVar('TAssemblyStaticLoad', bound='_6070.AbstractAssemblyLoadCase')


class AbstractAssemblyStaticLoadCaseGroup(_5272.PartStaticLoadCaseGroup, Generic[TAssembly, TAssemblyStaticLoad]):
    '''AbstractAssemblyStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TAssembly
        TAssemblyStaticLoad
    '''

    TYPE = _ABSTRACT_ASSEMBLY_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def part(self) -> 'TAssembly':
        '''TAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def assembly(self) -> 'TAssembly':
        '''TAssembly: 'Assembly' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TAssembly)(self.wrapped.Assembly) if self.wrapped.Assembly else None

    @property
    def part_load_cases(self) -> 'List[TAssemblyStaticLoad]':
        '''List[TAssemblyStaticLoad]: 'PartLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartLoadCases, constructor.new(TAssemblyStaticLoad))
        return value

    @property
    def assembly_load_cases(self) -> 'List[TAssemblyStaticLoad]':
        '''List[TAssemblyStaticLoad]: 'AssemblyLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyLoadCases, constructor.new(TAssemblyStaticLoad))
        return value
