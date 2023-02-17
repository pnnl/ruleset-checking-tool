from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.utils.jsonpath_utils import find_one

FAN_SYSTEM_SUPPLY_FAN_CONTROL = schema_enums["FanSystemSupplyFanControlOptions"]


def is_hvac_sys_fan_sys_cv(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system fan system is constant volume. Returns FALSE if the HVAC system fan system is anything other than constant volume.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the HVAC system fan system has constant volume
        False: the HVAC system has a fan system that is anything other than constant volume
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    return (
        find_one("$.fan_system.fan_control", hvac_b)
        == FAN_SYSTEM_SUPPLY_FAN_CONTROL.CONSTANT
    )
