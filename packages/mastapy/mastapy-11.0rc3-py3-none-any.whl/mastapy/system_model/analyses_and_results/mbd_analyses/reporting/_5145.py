﻿'''_5145.py

DynamicForceVector3DResult
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5144
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DYNAMIC_FORCE_VECTOR_3D_RESULT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Reporting', 'DynamicForceVector3DResult')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicForceVector3DResult',)


class DynamicForceVector3DResult(_0.APIBase):
    '''DynamicForceVector3DResult

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_FORCE_VECTOR_3D_RESULT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicForceVector3DResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def x(self) -> '_5144.DynamicForceResultAtTime':
        '''DynamicForceResultAtTime: 'X' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5144.DynamicForceResultAtTime)(self.wrapped.X) if self.wrapped.X else None

    @property
    def y(self) -> '_5144.DynamicForceResultAtTime':
        '''DynamicForceResultAtTime: 'Y' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5144.DynamicForceResultAtTime)(self.wrapped.Y) if self.wrapped.Y else None

    @property
    def z(self) -> '_5144.DynamicForceResultAtTime':
        '''DynamicForceResultAtTime: 'Z' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5144.DynamicForceResultAtTime)(self.wrapped.Z) if self.wrapped.Z else None

    @property
    def magnitude(self) -> '_5144.DynamicForceResultAtTime':
        '''DynamicForceResultAtTime: 'Magnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5144.DynamicForceResultAtTime)(self.wrapped.Magnitude) if self.wrapped.Magnitude else None

    @property
    def magnitude_xy(self) -> '_5144.DynamicForceResultAtTime':
        '''DynamicForceResultAtTime: 'MagnitudeXY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5144.DynamicForceResultAtTime)(self.wrapped.MagnitudeXY) if self.wrapped.MagnitudeXY else None
