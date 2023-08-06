﻿'''_4883.py

ModalCMSResultsForModeAndFE
'''


from mastapy._internal import constructor
from mastapy.nodal_analysis.component_mode_synthesis import _1525
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MODAL_CMS_RESULTS_FOR_MODE_AND_FE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'ModalCMSResultsForModeAndFE')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalCMSResultsForModeAndFE',)


class ModalCMSResultsForModeAndFE(_0.APIBase):
    '''ModalCMSResultsForModeAndFE

    This is a mastapy class.
    '''

    TYPE = _MODAL_CMS_RESULTS_FOR_MODE_AND_FE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalCMSResultsForModeAndFE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fe_name(self) -> 'str':
        '''str: 'FEName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEName

    @property
    def modal_full_fe_results(self) -> '_1525.ModalCMSResults':
        '''ModalCMSResults: 'ModalFullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1525.ModalCMSResults)(self.wrapped.ModalFullFEResults) if self.wrapped.ModalFullFEResults else None
