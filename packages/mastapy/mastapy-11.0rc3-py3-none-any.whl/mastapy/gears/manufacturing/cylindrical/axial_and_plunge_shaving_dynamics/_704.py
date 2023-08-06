﻿'''_704.py

PlungeShaverRedressing
'''


from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _711, _702
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_REDRESSING = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'PlungeShaverRedressing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverRedressing',)


class PlungeShaverRedressing(_711.ShaverRedressing['_702.PlungeShaverDynamics']):
    '''PlungeShaverRedressing

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_REDRESSING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverRedressing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
