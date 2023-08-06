﻿'''_1449.py

BarElasticMBD
'''


from mastapy.nodal_analysis.nodal_entities import _1450
from mastapy._internal.python_net import python_net_import

_BAR_ELASTIC_MBD = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'BarElasticMBD')


__docformat__ = 'restructuredtext en'
__all__ = ('BarElasticMBD',)


class BarElasticMBD(_1450.BarMBD):
    '''BarElasticMBD

    This is a mastapy class.
    '''

    TYPE = _BAR_ELASTIC_MBD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BarElasticMBD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
