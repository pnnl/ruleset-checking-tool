from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.utility_functions import (
    find_exactly_one_child_loop,
    find_exactly_one_fluid_loop,
    find_exactly_one_hvac_system,
)

FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]


def is_hvac_sys_fluid_loop_attached_to_chiller(rmd_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller
        False: otherwise
    """
    is_hvac_sys_fluid_loop_attached_to_chiller_flag = False
    chillers = find_all("$.chillers[*]", rmd_b)
    primary_cooling_loop_ids = [
        getattr_(chiller_b, "chiller", "cooling_loop") for chiller_b in chillers
    ]
    secondary_cooling_loop_ids = [
        secondary_loop["id"]
        for primary_cooling_loop_id in primary_cooling_loop_ids
        for secondary_loop in find_all(
            "$.child_loops[*]",
            find_exactly_one_fluid_loop(rmd_b, primary_cooling_loop_id),
        )
    ]

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)

    # Allow single loop and primary/secondary loop configuration as true.
    chilled_water_loop_id = find_one("cooling_system.chilled_water_loop", hvac_b)
    water_loop = None
    if chilled_water_loop_id in primary_cooling_loop_ids:
        water_loop = find_exactly_one_fluid_loop(rmd_b, chilled_water_loop_id)
    elif chilled_water_loop_id in secondary_cooling_loop_ids:
        water_loop = find_exactly_one_child_loop(rmd_b, chilled_water_loop_id)
    is_hvac_sys_fluid_loop_attached_to_chiller_flag = (
        water_loop is not None and find_one("type", water_loop) == FLUID_LOOP.COOLING
    )

    return is_hvac_sys_fluid_loop_attached_to_chiller_flag
