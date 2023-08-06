﻿'''_968.py

CylindricalPlanetGearDesign
'''


from typing import List

from mastapy.geometry.two_d import _273
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears import _301
from mastapy.gears.gear_designs.cylindrical import _992, _991, _942
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalPlanetGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearDesign',)


class CylindricalPlanetGearDesign(_942.CylindricalGearDesign):
    '''CylindricalPlanetGearDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def internal_external(self) -> '_273.InternalExternalType':
        '''InternalExternalType: 'InternalExternal' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.InternalExternal)
        return constructor.new(_273.InternalExternalType)(value) if value else None

    @internal_external.setter
    def internal_external(self, value: '_273.InternalExternalType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InternalExternal = value

    @property
    def has_factorising_sun(self) -> 'bool':
        '''bool: 'HasFactorisingSun' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasFactorisingSun

    @property
    def has_factorising_annulus(self) -> 'bool':
        '''bool: 'HasFactorisingAnnulus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasFactorisingAnnulus

    @property
    def planetary_details(self) -> '_301.PlanetaryDetail':
        '''PlanetaryDetail: 'PlanetaryDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_301.PlanetaryDetail)(self.wrapped.PlanetaryDetails) if self.wrapped.PlanetaryDetails else None

    @property
    def planetary_sidebands_amplitude_factors(self) -> 'List[_992.NamedPlanetSideBandAmplitudeFactor]':
        '''List[NamedPlanetSideBandAmplitudeFactor]: 'PlanetarySidebandsAmplitudeFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetarySidebandsAmplitudeFactors, constructor.new(_992.NamedPlanetSideBandAmplitudeFactor))
        return value

    @property
    def planet_assembly_indices(self) -> 'List[_991.NamedPlanetAssemblyIndex]':
        '''List[NamedPlanetAssemblyIndex]: 'PlanetAssemblyIndices' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetAssemblyIndices, constructor.new(_991.NamedPlanetAssemblyIndex))
        return value
