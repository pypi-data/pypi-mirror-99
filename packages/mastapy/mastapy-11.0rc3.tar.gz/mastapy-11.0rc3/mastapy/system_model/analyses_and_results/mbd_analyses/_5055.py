﻿'''_5055.py

BoltMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6467
from mastapy.system_model.analyses_and_results.mbd_analyses import _5061
from mastapy._internal.python_net import python_net_import

_BOLT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BoltMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltMultibodyDynamicsAnalysis',)


class BoltMultibodyDynamicsAnalysis(_5061.ComponentMultibodyDynamicsAnalysis):
    '''BoltMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6467.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6467.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
