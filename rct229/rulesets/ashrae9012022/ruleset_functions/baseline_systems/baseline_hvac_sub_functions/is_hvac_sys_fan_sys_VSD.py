from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import find_exactly_one_hvac_system

FAN_SYSTEM_SUPPLY_FAN_CONTROL = SchemaEnums.schema_enums[
    "FanSystemSupplyFanControlOptions"
]


def is_hvac_sys_fan_sys_vsd(rmd_b, hvac_b_id):
    """Returns TRUE if the HVAC system fan system is variable speed drive controlled. Returns FALSE if the HVAC system fan system is anything other than variable speed drive controlled.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system fan system his variable speed drive control
        False: the HVAC system has a fan system that is anything other than variable speed drive controlled
    """

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)
    fan_system = hvac_b.get("fan_system")
    is_hvac_sys_fan_sys_vsd_flag = (
        fan_system is not None
        and fan_system.get("fan_control")
        == FAN_SYSTEM_SUPPLY_FAN_CONTROL.VARIABLE_SPEED_DRIVE
    )

    return is_hvac_sys_fan_sys_vsd_flag
