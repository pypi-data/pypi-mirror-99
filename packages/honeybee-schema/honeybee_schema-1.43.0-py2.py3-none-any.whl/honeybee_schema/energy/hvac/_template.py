"""Base class for HVAC systems following a standards template."""
from pydantic import Field
from enum import Enum

from .._base import IDdEnergyBaseModel


class Vintages(str, Enum):
    ashrae_2013 = 'ASHRAE_2013'
    ashrae_2010 = 'ASHRAE_2010'
    ashrae_2007 = 'ASHRAE_2007'
    ashrae_2004 = 'ASHRAE_2004'
    doe_ref_1980_2004 = 'DOE_Ref_1980_2004'
    doe_ref_pre_1980 = 'DOE_Ref_Pre_1980'


class _TemplateSystem(IDdEnergyBaseModel):
    """Base class for HVAC systems following a standards template."""

    vintage: Vintages = Field(
        Vintages.ashrae_2013,
        description='Text for the vintage of the template system. This will be used '
        'to set efficiencies for various pieces of equipment within the system. '
        'Further information about these defaults can be found in the version of '
        'ASHRAE 90.1 corresponding to the selected vintage. Read-only versions '
        'of the standard can be found at: https://www.ashrae.org/technical-resources/'
        'standards-and-guidelines/read-only-versions-of-ashrae-standards'
    )
