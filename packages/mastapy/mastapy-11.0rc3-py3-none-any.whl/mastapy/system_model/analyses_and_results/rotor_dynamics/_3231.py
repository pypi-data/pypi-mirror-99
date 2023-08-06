﻿'''_3231.py

ShaftModalComplexShape
'''


from mastapy.system_model.analyses_and_results.rotor_dynamics import _3229
from mastapy.utility.units_and_measurements.measurements import _1224
from mastapy._internal.python_net import python_net_import

_SHAFT_MODAL_COMPLEX_SHAPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics', 'ShaftModalComplexShape')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftModalComplexShape',)


class ShaftModalComplexShape(_3229.ShaftComplexShape['_1224.Number', 'SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements.Number']):
    '''ShaftModalComplexShape

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MODAL_COMPLEX_SHAPE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftModalComplexShape.TYPE'):
        super().__init__(instance_to_wrap)
