from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.utility_functions import (
    find_exactly_one_fluid_loop,
    find_exactly_one_hvac_system,
)

FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]


def is_hvac_sys_fluid_loop_attached_to_boiler(rmd_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler
        False: otherwise
    """
    is_hvac_sys_fluid_loop_attached_to_boiler_flag = False
    boiler_loop_ids = find_all("$.boilers[*].loop", rmd_b)
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)
    hot_water_loop_id = find_one("heating_system.hot_water_loop", hvac_b)
    if hot_water_loop_id in boiler_loop_ids:
        hot_water_loop = find_exactly_one_fluid_loop(rmd_b, hot_water_loop_id)
        is_hvac_sys_fluid_loop_attached_to_boiler_flag = (
            find_one("type", hot_water_loop) == FLUID_LOOP.HEATING
        )

    return is_hvac_sys_fluid_loop_attached_to_boiler_flag
