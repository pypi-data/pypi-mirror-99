﻿'''_4808.py

FEPartModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6523
from mastapy.system_model.analyses_and_results.system_deflections import _2423
from mastapy.nodal_analysis.component_mode_synthesis import _201
from mastapy.system_model.analyses_and_results.modal_analyses import _4753
from mastapy._internal.python_net import python_net_import

_FE_PART_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'FEPartModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartModalAnalysis',)


class FEPartModalAnalysis(_4753.AbstractShaftOrHousingModalAnalysis):
    '''FEPartModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2130.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6523.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6523.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2423.FEPartSystemDeflection':
        '''FEPartSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2423.FEPartSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[FEPartModalAnalysis]':
        '''List[FEPartModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartModalAnalysis))
        return value

    @property
    def modal_full_fe_results(self) -> 'List[_201.ModalCMSResults]':
        '''List[ModalCMSResults]: 'ModalFullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ModalFullFEResults, constructor.new(_201.ModalCMSResults))
        return value

    def calculate_mode_shapes(self):
        ''' 'CalculateModeShapes' is the original name of this method.'''

        self.wrapped.CalculateModeShapes()

    def calculate_selected_strain_and_kinetic_energy(self):
        ''' 'CalculateSelectedStrainAndKineticEnergy' is the original name of this method.'''

        self.wrapped.CalculateSelectedStrainAndKineticEnergy()

    def calculate_all_strain_and_kinetic_energies(self):
        ''' 'CalculateAllStrainAndKineticEnergies' is the original name of this method.'''

        self.wrapped.CalculateAllStrainAndKineticEnergies()
