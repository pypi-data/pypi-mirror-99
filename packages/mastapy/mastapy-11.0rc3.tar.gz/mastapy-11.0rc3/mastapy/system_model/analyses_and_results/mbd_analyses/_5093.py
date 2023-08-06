﻿'''_5093.py

FlexiblePinAssemblyMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2131
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6524
from mastapy.system_model.analyses_and_results.mbd_analyses import _5145
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'FlexiblePinAssemblyMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyMultibodyDynamicsAnalysis',)


class FlexiblePinAssemblyMultibodyDynamicsAnalysis(_5145.SpecialisedAssemblyMultibodyDynamicsAnalysis):
    '''FlexiblePinAssemblyMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2131.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2131.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6524.FlexiblePinAssemblyLoadCase':
        '''FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6524.FlexiblePinAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
