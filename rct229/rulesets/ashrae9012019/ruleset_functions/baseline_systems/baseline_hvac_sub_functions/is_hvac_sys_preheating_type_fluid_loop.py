from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_hvac_sys_preheating_type_fluid_loop(rmd_b: dict, hvac_b_id: str) -> bool:
    """Returns TRUE if the HVAC system preheating system heating type is fluid loop. Returns FALSE if the HVAC system
    preheating system has anything other than fluid loop.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system preheating system has fluid loop as the heating type
        False: otherwise
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)
    # get preheat system from the HVAC
    preheat_system = hvac_b.get("preheat_system")
    is_hvac_sys_preheating_type_fluid_loop_flag = (
        preheat_system is not None
        and preheat_system.get("hot_water_loop") is not None
        # Silence fail if heating system type data is not in RMD
        and find_one("$.type", preheat_system) == HEATING_SYSTEM.FLUID_LOOP
    )

    return is_hvac_sys_preheating_type_fluid_loop_flag
