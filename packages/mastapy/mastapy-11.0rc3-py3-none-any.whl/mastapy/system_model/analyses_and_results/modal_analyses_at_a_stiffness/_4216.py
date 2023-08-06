﻿'''_4216.py

BevelDifferentialSunGearModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.gears import _2164
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4213
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'BevelDifferentialSunGearModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearModalAnalysisAtAStiffness',)


class BevelDifferentialSunGearModalAnalysisAtAStiffness(_4213.BevelDifferentialGearModalAnalysisAtAStiffness):
    '''BevelDifferentialSunGearModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2164.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2164.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
