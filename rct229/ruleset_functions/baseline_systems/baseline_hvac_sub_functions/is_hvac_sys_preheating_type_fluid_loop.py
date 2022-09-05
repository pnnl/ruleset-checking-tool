from rct229.data.schema_enums import schema_enums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_hvac_sys_preheating_type_fluid_loop(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system preheating system heating type is fluid loop. Returns FALSE if the HVAC system
    preheating system has anything other than fluid loop.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system preheating system has fluid loop as the heating type
        False: otherwise
    """
    is_hvac_sys_preheating_type_fluid_loop_flag = False

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
        "id",
        hvac_b_id,
        rmi_b,
    )
    # get preheat system from the HVAC
    preheat_system = hvac_b.get("preheat_system")
    is_hvac_sys_preheating_type_fluid_loop_flag = (
        preheat_system is not None
        and preheat_system.get("hot_water_loop") is not None
        and getattr_(preheat_system, "preheat_system", "heating_system_type")
        == HEATING_SYSTEM.FLUID_LOOP
    )

    return is_hvac_sys_preheating_type_fluid_loop_flag
