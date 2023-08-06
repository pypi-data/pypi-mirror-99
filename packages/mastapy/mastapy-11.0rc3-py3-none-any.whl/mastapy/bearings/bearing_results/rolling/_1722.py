﻿'''_1722.py

LoadedNonBarrelRollerBearingStripLoadResults
'''


from mastapy.bearings.bearing_results.rolling import _1727
from mastapy._internal.python_net import python_net_import

_LOADED_NON_BARREL_ROLLER_BEARING_STRIP_LOAD_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedNonBarrelRollerBearingStripLoadResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNonBarrelRollerBearingStripLoadResults',)


class LoadedNonBarrelRollerBearingStripLoadResults(_1727.LoadedRollerStripLoadResults):
    '''LoadedNonBarrelRollerBearingStripLoadResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_NON_BARREL_ROLLER_BEARING_STRIP_LOAD_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedNonBarrelRollerBearingStripLoadResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
