﻿'''_3362.py

PowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2399
from mastapy.system_model.analyses_and_results.analysis_cases import _6566
from mastapy._internal.python_net import python_net_import

_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerFlow',)


class PowerFlow(_6566.StaticLoadAnalysisCase):
    '''PowerFlow

    This is a mastapy class.
    '''

    TYPE = _POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ratio(self) -> 'float':
        '''float: 'Ratio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Ratio

    @property
    def torsional_system_deflection(self) -> '_2399.TorsionalSystemDeflection':
        '''TorsionalSystemDeflection: 'TorsionalSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2399.TorsionalSystemDeflection)(self.wrapped.TorsionalSystemDeflection) if self.wrapped.TorsionalSystemDeflection else None
