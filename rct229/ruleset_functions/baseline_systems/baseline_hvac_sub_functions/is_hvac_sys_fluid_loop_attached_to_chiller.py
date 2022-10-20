from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
    find_exactly_one_fluid_loop,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one

FLUID_LOOP = schema_enums["FluidLoopOptions"]


def is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller
        False: otherwise
    """
    is_hvac_sys_fluid_loop_attached_to_chiller_flag = False
    chillers = find_all("$.chillers[*]", rmi_b)
    cooling_loop_ids = [
        getattr_(chiller_b, "chiller", "cooling_loop") for chiller_b in chillers
    ]

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    chilled_water_loop_id = find_one("cooling_system.chilled_water_loop", hvac_b)
    if chilled_water_loop_id in cooling_loop_ids:
        chilled_water_loop = find_exactly_one_fluid_loop(rmi_b, chilled_water_loop_id)
        is_hvac_sys_fluid_loop_attached_to_chiller_flag = (
            find_one("type", chilled_water_loop) == FLUID_LOOP.COOLING
        )

    return is_hvac_sys_fluid_loop_attached_to_chiller_flag
