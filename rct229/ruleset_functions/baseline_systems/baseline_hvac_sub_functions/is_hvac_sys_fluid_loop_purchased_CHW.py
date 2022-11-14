from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.utils.jsonpath_utils import find_all, find_one

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]


def is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to an external purchased chilled water loop. Returns FALSE if this is not the case.
    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.
    Returns
    -------
    bool
        True: the fluid loop associated with the cooling system associated with the HVAC system is attached to an external purchased cooling loop
        False: otherwise
    """
    purchased_cooling_loop_id_list_b = [
        *find_all(
            f'external_fluid_source[*][?(@.type="{EXTERNAL_FLUID_SOURCE.CHILLED_WATER}")].loop',
            rmi_b,
        )
    ]

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)
    # the hvac_sys has a cooling system and the cooling system has a chilled_water_loop and
    # the loop id is in the purchased_cooling_loop_id_list
    is_hvac_sys_fluid_loop_purchased_chw_flag = (
        find_one("cooling_system.chilled_water_loop", hvac_b)
        in purchased_cooling_loop_id_list_b
    )

    return is_hvac_sys_fluid_loop_purchased_chw_flag
