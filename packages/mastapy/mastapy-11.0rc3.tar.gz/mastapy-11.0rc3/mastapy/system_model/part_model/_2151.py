﻿'''_2151.py

RootAssembly
'''


from typing import List

from mastapy.system_model import _1887
from mastapy._internal import constructor, conversion
from mastapy.geometry import _272
from mastapy.system_model.part_model.projections import _2161
from mastapy.system_model.part_model.part_groups import _2166
from mastapy.system_model.part_model import _2112
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssembly',)


class RootAssembly(_2112.Assembly):
    '''RootAssembly

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def model(self) -> '_1887.Design':
        '''Design: 'Model' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1887.Design)(self.wrapped.Model) if self.wrapped.Model else None

    @property
    def packaging_limits(self) -> '_272.PackagingLimits':
        '''PackagingLimits: 'PackagingLimits' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_272.PackagingLimits)(self.wrapped.PackagingLimits) if self.wrapped.PackagingLimits else None

    @property
    def parallel_part_groups_drawing_order(self) -> 'List[_2161.SpecifiedParallelPartGroupDrawingOrder]':
        '''List[SpecifiedParallelPartGroupDrawingOrder]: 'ParallelPartGroupsDrawingOrder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroupsDrawingOrder, constructor.new(_2161.SpecifiedParallelPartGroupDrawingOrder))
        return value

    @property
    def parallel_part_groups(self) -> 'List[_2166.ParallelPartGroup]':
        '''List[ParallelPartGroup]: 'ParallelPartGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroups, constructor.new(_2166.ParallelPartGroup))
        return value

    def attempt_to_fix_all_gear_sets(self):
        ''' 'AttemptToFixAllGearSets' is the original name of this method.'''

        self.wrapped.AttemptToFixAllGearSets()

    def attempt_to_fix_all_cylindrical_gear_sets_by_changing_normal_module(self):
        ''' 'AttemptToFixAllCylindricalGearSetsByChangingNormalModule' is the original name of this method.'''

        self.wrapped.AttemptToFixAllCylindricalGearSetsByChangingNormalModule()

    def set_packaging_limits_to_current_bounding_box(self):
        ''' 'SetPackagingLimitsToCurrentBoundingBox' is the original name of this method.'''

        self.wrapped.SetPackagingLimitsToCurrentBoundingBox()

    def set_packaging_limits_to_current_bounding_box_of_all_gears(self):
        ''' 'SetPackagingLimitsToCurrentBoundingBoxOfAllGears' is the original name of this method.'''

        self.wrapped.SetPackagingLimitsToCurrentBoundingBoxOfAllGears()

    def open_fe_substructure_version_comparer(self):
        ''' 'OpenFESubstructureVersionComparer' is the original name of this method.'''

        self.wrapped.OpenFESubstructureVersionComparer()
