from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

COOLING_SYSTEM_TYPE = SchemaEnums.schema_enums["CoolingSystemOptions"]


def is_hvac_sys_cooling_type_fluid_loop(rmd_b, hvac_b_id):
    """Returns TRUE if the HVAC system has fluid_loop cooling. Returns FALSE if the HVAC system has anything other
    than fluid_loop cooling or if it has more than 1 cooling system.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system has fluid_loop cooling
        False: HVAC system has a cooling system type other than fluid_loop
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)
    # Check if hvac_b has preheat system
    cooling_system = hvac_b.get("cooling_system")
    is_hvac_sys_cooling_type_fluid_loop_flag = (
        cooling_system is not None
        and cooling_system.get("chilled_water_loop") is not None
        and find_one("type", cooling_system) == COOLING_SYSTEM_TYPE.FLUID_LOOP
    )

    return is_hvac_sys_cooling_type_fluid_loop_flag
