﻿'''_796.py

CylindricalGearSetLoadDistributionAnalysis
'''


from typing import List

from mastapy.gears.rating.cylindrical import _423
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_two_d_fe_analysis import _831
from mastapy.gears.ltca.cylindrical import _793
from mastapy.gears.ltca import _783
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearSetLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetLoadDistributionAnalysis',)


class CylindricalGearSetLoadDistributionAnalysis(_783.GearSetLoadDistributionAnalysis):
    '''CylindricalGearSetLoadDistributionAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> '_423.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_423.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def tiff_analysis(self) -> '_831.CylindricalGearSetTIFFAnalysis':
        '''CylindricalGearSetTIFFAnalysis: 'TIFFAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_831.CylindricalGearSetTIFFAnalysis)(self.wrapped.TIFFAnalysis) if self.wrapped.TIFFAnalysis else None

    @property
    def meshes(self) -> 'List[_793.CylindricalGearMeshLoadDistributionAnalysis]':
        '''List[CylindricalGearMeshLoadDistributionAnalysis]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Meshes, constructor.new(_793.CylindricalGearMeshLoadDistributionAnalysis))
        return value
