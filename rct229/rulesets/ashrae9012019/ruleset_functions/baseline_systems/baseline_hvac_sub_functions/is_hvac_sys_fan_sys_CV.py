from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

FAN_SYSTEM_SUPPLY_FAN_CONTROL = SchemaEnums.schema_enums[
    "FanSystemSupplyFanControlOptions"
]


def is_hvac_sys_fan_sys_cv(rmd_b, hvac_b_id):
    """Returns TRUE if the HVAC system fan system is constant volume. Returns FALSE if the HVAC system fan system is anything other than constant volume.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the HVAC system fan system has constant volume
        False: the HVAC system has a fan system that is anything other than constant volume
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)

    return (
        find_one("$.fan_system.fan_control", hvac_b)
        == FAN_SYSTEM_SUPPLY_FAN_CONTROL.CONSTANT
    )
