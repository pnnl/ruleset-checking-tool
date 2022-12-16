from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.utils.jsonpath_utils import find_one

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_hvac_sys_heating_type_fluid_loop(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system heating system heating type is fluid loop. Returns FALSE if the HVAC system
    heating system has anything other than fluid loop or if it has more than 1 heating system.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system heating system has fluid loop as the heating type
        False: HVAC system has a heating system type other than fluid loop
    """
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)
    heating_system = hvac_b.get("heating_system")
    is_hvac_sys_heating_type_fluid_loop_flag = (
        heating_system is not None
        and heating_system.get("hot_water_loop") is not None
        and find_one("heating_system_type", heating_system) == HEATING_SYSTEM.FLUID_LOOP
    )

    return is_hvac_sys_heating_type_fluid_loop_flag
