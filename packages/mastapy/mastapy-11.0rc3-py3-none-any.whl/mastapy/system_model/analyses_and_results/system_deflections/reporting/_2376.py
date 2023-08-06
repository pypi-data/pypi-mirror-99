﻿'''_2376.py

RigidlyConnectedComponentGroupSystemDeflection
'''


from typing import List

from mastapy.math_utility import _1082
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2253
from mastapy.system_model.analyses_and_results import _2204
from mastapy._internal.python_net import python_net_import

_RIGIDLY_CONNECTED_COMPONENT_GROUP_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting', 'RigidlyConnectedComponentGroupSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidlyConnectedComponentGroupSystemDeflection',)


class RigidlyConnectedComponentGroupSystemDeflection(_2204.DesignEntityGroupAnalysis):
    '''RigidlyConnectedComponentGroupSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _RIGIDLY_CONNECTED_COMPONENT_GROUP_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RigidlyConnectedComponentGroupSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mass_properties(self) -> '_1082.MassProperties':
        '''MassProperties: 'MassProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1082.MassProperties)(self.wrapped.MassProperties) if self.wrapped.MassProperties else None

    @property
    def components(self) -> 'List[_2253.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'Components' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Components, constructor.new(_2253.ComponentSystemDeflection))
        return value
