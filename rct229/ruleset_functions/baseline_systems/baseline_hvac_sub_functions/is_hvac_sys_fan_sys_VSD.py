from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

FAN_SYSTEM_SUPPLY_FAN_CONTROL = schema_enums["FanSystemSupplyFanControlOptions"]


def is_hvac_sys_fan_sys_vsd(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system fan system is variable speed drive controlled. Returns FALSE if the HVAC system fan system is anything other than variable speed drive controlled.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system fan system his variable speed drive control
        False: the HVAC system has a fan system that is anything other than variable speed drive controlled
    """
    is_hvac_sys_fan_sys_vsd_flag = False

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems[*]",
        "id",
        hvac_b_id,
        rmi_b,
    )
    fan_system = hvac_b.get("fan_system")
    is_hvac_sys_fan_sys_vsd_flag = (
        fan_system is not None
        and fan_system.get("fan_control")
        == FAN_SYSTEM_SUPPLY_FAN_CONTROL.VARIABLE_SPEED_DRIVE
    )

    return is_hvac_sys_fan_sys_vsd_flag
