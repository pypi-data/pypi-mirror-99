﻿'''_1295.py

CustomImage
'''


from mastapy.utility.report import _1294
from mastapy._internal.python_net import python_net_import

_CUSTOM_IMAGE = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomImage')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomImage',)


class CustomImage(_1294.CustomGraphic):
    '''CustomImage

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_IMAGE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomImage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
