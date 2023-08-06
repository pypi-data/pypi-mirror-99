﻿'''_1560.py

ProfileDataToUse
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PROFILE_DATA_TO_USE = python_net_import('SMT.MastaAPI.Bearings.RollerBearingProfiles', 'ProfileDataToUse')


__docformat__ = 'restructuredtext en'
__all__ = ('ProfileDataToUse',)


class ProfileDataToUse(Enum):
    '''ProfileDataToUse

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _PROFILE_DATA_TO_USE

    __hash__ = None

    ACTUAL_DATA = 0
    SMOOTHED = 1
    FITTED_STANDARD_PROFILE = 2
