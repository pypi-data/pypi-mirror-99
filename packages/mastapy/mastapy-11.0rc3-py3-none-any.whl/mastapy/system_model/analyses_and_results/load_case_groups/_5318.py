﻿'''_5318.py

ConceptSynchroGearEngagementStatus
'''


from mastapy.system_model.analyses_and_results.load_case_groups import _5321
from mastapy.system_model.part_model.gears import _2200
from mastapy._internal.python_net import python_net_import

_CONCEPT_SYNCHRO_GEAR_ENGAGEMENT_STATUS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'ConceptSynchroGearEngagementStatus')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptSynchroGearEngagementStatus',)


class ConceptSynchroGearEngagementStatus(_5321.GenericClutchEngagementStatus['_2200.CylindricalGear']):
    '''ConceptSynchroGearEngagementStatus

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_SYNCHRO_GEAR_ENGAGEMENT_STATUS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptSynchroGearEngagementStatus.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
