﻿'''_2482.py

ShaftSystemDeflectionSectionsReport
'''


from mastapy.utility.enums import _1462
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility.report import _1404
from mastapy._internal.python_net import python_net_import

_SHAFT_SYSTEM_DEFLECTION_SECTIONS_REPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting', 'ShaftSystemDeflectionSectionsReport')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSystemDeflectionSectionsReport',)


class ShaftSystemDeflectionSectionsReport(_1404.CustomReportChart):
    '''ShaftSystemDeflectionSectionsReport

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SYSTEM_DEFLECTION_SECTIONS_REPORT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSystemDeflectionSectionsReport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def display(self) -> '_1462.TableAndChartOptions':
        '''TableAndChartOptions: 'Display' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Display)
        return constructor.new(_1462.TableAndChartOptions)(value) if value else None

    @display.setter
    def display(self, value: '_1462.TableAndChartOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Display = value
