﻿'''_5388.py

GearMeshTEExcitationDetail
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5385
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_TE_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearMeshTEExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshTEExcitationDetail',)


class GearMeshTEExcitationDetail(_5385.GearMeshExcitationDetail):
    '''GearMeshTEExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_TE_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshTEExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
