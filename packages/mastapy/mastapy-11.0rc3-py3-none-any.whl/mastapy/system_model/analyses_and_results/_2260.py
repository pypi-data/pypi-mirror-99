﻿'''_2260.py

CompoundMultibodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundMultibodyDynamicsAnalysis',)


class CompoundMultibodyDynamicsAnalysis(_2213.CompoundAnalysis):
    '''CompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
