﻿'''_4838.py

PartToPartShearCouplingHalfModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2264
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6568
from mastapy.system_model.analyses_and_results.system_deflections import _2453
from mastapy.system_model.analyses_and_results.modal_analyses import _4790
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PartToPartShearCouplingHalfModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfModalAnalysis',)


class PartToPartShearCouplingHalfModalAnalysis(_4790.CouplingHalfModalAnalysis):
    '''PartToPartShearCouplingHalfModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2264.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2264.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6568.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6568.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2453.PartToPartShearCouplingHalfSystemDeflection':
        '''PartToPartShearCouplingHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2453.PartToPartShearCouplingHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
