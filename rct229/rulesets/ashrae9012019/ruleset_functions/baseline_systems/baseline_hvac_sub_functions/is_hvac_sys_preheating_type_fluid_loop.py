from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.utils.jsonpath_utils import find_one

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
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)
    # get preheat system from the HVAC
    preheat_system = hvac_b.get("preheat_system")
    is_hvac_sys_preheating_type_fluid_loop_flag = (
        preheat_system is not None
        and preheat_system.get("hot_water_loop") is not None
        # Silence fail if heating system type data is not in RMD
        and find_one("type", preheat_system) == HEATING_SYSTEM.FLUID_LOOP
    )

    return is_hvac_sys_preheating_type_fluid_loop_flag
