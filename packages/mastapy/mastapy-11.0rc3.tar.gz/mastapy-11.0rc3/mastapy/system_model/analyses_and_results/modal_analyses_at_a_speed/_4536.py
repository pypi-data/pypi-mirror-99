﻿'''_4536.py

CycloidalAssemblyModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.cycloidal import _2243
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6492
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4591
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'CycloidalAssemblyModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyModalAnalysisAtASpeed',)


class CycloidalAssemblyModalAnalysisAtASpeed(_4591.SpecialisedAssemblyModalAnalysisAtASpeed):
    '''CycloidalAssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2243.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2243.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6492.CycloidalAssemblyLoadCase':
        '''CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6492.CycloidalAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
