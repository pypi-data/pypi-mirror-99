﻿'''_6159.py

CVTLoadCase
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2180
from mastapy.system_model.analyses_and_results.static_loads import _6160, _6126
from mastapy._internal.python_net import python_net_import

_CVT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CVTLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTLoadCase',)


class CVTLoadCase(_6126.BeltDriveLoadCase):
    '''CVTLoadCase

    This is a mastapy class.
    '''

    TYPE = _CVT_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def speed_ratio(self) -> 'float':
        '''float: 'SpeedRatio' is the original name of this property.'''

        return self.wrapped.SpeedRatio

    @speed_ratio.setter
    def speed_ratio(self, value: 'float'):
        self.wrapped.SpeedRatio = float(value) if value else 0.0

    @property
    def assembly_design(self) -> '_2180.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def pulleys(self) -> 'List[_6160.CVTPulleyLoadCase]':
        '''List[CVTPulleyLoadCase]: 'Pulleys' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Pulleys, constructor.new(_6160.CVTPulleyLoadCase))
        return value
