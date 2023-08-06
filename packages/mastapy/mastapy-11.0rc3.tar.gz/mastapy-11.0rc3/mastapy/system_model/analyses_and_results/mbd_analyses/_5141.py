﻿'''_5141.py

ShaftHubConnectionMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2273
from mastapy.system_model.analyses_and_results.static_loads import _6587
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5181, _5183
from mastapy.system_model.analyses_and_results.mbd_analyses import _5072
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ShaftHubConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionMultibodyDynamicsAnalysis',)


class ShaftHubConnectionMultibodyDynamicsAnalysis(_5072.ConnectorMultibodyDynamicsAnalysis):
    '''ShaftHubConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def force(self) -> 'Vector3D':
        '''Vector3D: 'Force' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Force)
        return value

    @property
    def force_angular(self) -> 'Vector3D':
        '''Vector3D: 'ForceAngular' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.ForceAngular)
        return value

    @property
    def relative_linear_displacement(self) -> 'Vector3D':
        '''Vector3D: 'RelativeLinearDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.RelativeLinearDisplacement)
        return value

    @property
    def relative_angular_displacement(self) -> 'Vector3D':
        '''Vector3D: 'RelativeAngularDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.RelativeAngularDisplacement)
        return value

    @property
    def component_design(self) -> '_2273.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6587.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6587.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def peak_dynamic_force(self) -> '_5181.DynamicForceVector3DResult':
        '''DynamicForceVector3DResult: 'PeakDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5181.DynamicForceVector3DResult)(self.wrapped.PeakDynamicForce) if self.wrapped.PeakDynamicForce else None

    @property
    def peak_dynamic_force_angular(self) -> '_5183.DynamicTorqueVector3DResult':
        '''DynamicTorqueVector3DResult: 'PeakDynamicForceAngular' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5183.DynamicTorqueVector3DResult)(self.wrapped.PeakDynamicForceAngular) if self.wrapped.PeakDynamicForceAngular else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionMultibodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionMultibodyDynamicsAnalysis))
        return value
