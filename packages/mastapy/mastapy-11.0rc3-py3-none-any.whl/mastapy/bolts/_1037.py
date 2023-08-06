﻿'''_1037.py

BoltedJointMaterial
'''


from mastapy._internal import constructor
from mastapy.materials import _74
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MATERIAL = python_net_import('SMT.MastaAPI.Bolts', 'BoltedJointMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointMaterial',)


class BoltedJointMaterial(_74.Material):
    '''BoltedJointMaterial

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_MATERIAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def stress_endurance_limit(self) -> 'float':
        '''float: 'StressEnduranceLimit' is the original name of this property.'''

        return self.wrapped.StressEnduranceLimit

    @stress_endurance_limit.setter
    def stress_endurance_limit(self, value: 'float'):
        self.wrapped.StressEnduranceLimit = float(value) if value else 0.0

    @property
    def limiting_surface_pressure(self) -> 'float':
        '''float: 'LimitingSurfacePressure' is the original name of this property.'''

        return self.wrapped.LimitingSurfacePressure

    @limiting_surface_pressure.setter
    def limiting_surface_pressure(self, value: 'float'):
        self.wrapped.LimitingSurfacePressure = float(value) if value else 0.0

    @property
    def shearing_strength(self) -> 'float':
        '''float: 'ShearingStrength' is the original name of this property.'''

        return self.wrapped.ShearingStrength

    @shearing_strength.setter
    def shearing_strength(self, value: 'float'):
        self.wrapped.ShearingStrength = float(value) if value else 0.0

    @property
    def proof_stress(self) -> 'float':
        '''float: 'ProofStress' is the original name of this property.'''

        return self.wrapped.ProofStress

    @proof_stress.setter
    def proof_stress(self, value: 'float'):
        self.wrapped.ProofStress = float(value) if value else 0.0

    @property
    def minimum_tensile_strength(self) -> 'float':
        '''float: 'MinimumTensileStrength' is the original name of this property.'''

        return self.wrapped.MinimumTensileStrength

    @minimum_tensile_strength.setter
    def minimum_tensile_strength(self, value: 'float'):
        self.wrapped.MinimumTensileStrength = float(value) if value else 0.0

    @property
    def modulus_of_elasticity_at_20c(self) -> 'float':
        '''float: 'ModulusOfElasticityAt20C' is the original name of this property.'''

        return self.wrapped.ModulusOfElasticityAt20C

    @modulus_of_elasticity_at_20c.setter
    def modulus_of_elasticity_at_20c(self, value: 'float'):
        self.wrapped.ModulusOfElasticityAt20C = float(value) if value else 0.0

    @property
    def coefficient_of_thermal_expansion_at_20c(self) -> 'float':
        '''float: 'CoefficientOfThermalExpansionAt20C' is the original name of this property.'''

        return self.wrapped.CoefficientOfThermalExpansionAt20C

    @coefficient_of_thermal_expansion_at_20c.setter
    def coefficient_of_thermal_expansion_at_20c(self, value: 'float'):
        self.wrapped.CoefficientOfThermalExpansionAt20C = float(value) if value else 0.0
