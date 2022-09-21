from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

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
        True: the HVAC system fan system his constant volume
        False: the HVAC system has a fan system that is anything other than constant volume
    """
    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems[*]",
        "id",
        hvac_b_id,
        rmi_b,
    )
    fan_system = hvac_b.get("fan_system")
    is_hvac_sys_fan_sys_cv_flag = (
        fan_system is not None
        and fan_system.get("fan_control")
        == FAN_SYSTEM_SUPPLY_FAN_CONTROL.CONSTANT
    )

    return is_hvac_sys_fan_sys_cv_flag
