﻿'''_6176.py

ElectricMachineHarmonicLoadDataFromMotorCAD
'''


from mastapy.system_model.analyses_and_results.static_loads import _6177, _6181
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_CAD = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadDataFromMotorCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadDataFromMotorCAD',)


class ElectricMachineHarmonicLoadDataFromMotorCAD(_6177.ElectricMachineHarmonicLoadDataFromMotorPackages['_6181.ElectricMachineHarmonicLoadMotorCADImportOptions']):
    '''ElectricMachineHarmonicLoadDataFromMotorCAD

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_CAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
