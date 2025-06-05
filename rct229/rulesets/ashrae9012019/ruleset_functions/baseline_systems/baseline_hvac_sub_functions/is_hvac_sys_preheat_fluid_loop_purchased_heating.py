from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_hvac_system

EXTERNAL_FLUID_SOURCE = SchemaEnums.schema_enums["ExternalFluidSourceOptions"]


def is_hvac_sys_preheat_fluid_loop_purchased_heating(rmd_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the preheating system associated with the HVAC system is
    attached to an external purchased heating loop. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: fluid loop associated with the preheating system associated with the HVAC system is attached to an external purchased heating loop
        False: otherwise
    """
    purchased_heating_loop_list_b = [
        *find_all(
            f'external_fluid_sources[*][?(@.type="{EXTERNAL_FLUID_SOURCE.HOT_WATER}"), ?(@.type="{EXTERNAL_FLUID_SOURCE.STEAM}")].loop',
            rmd_b,
        )
    ]

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)
    # Check if hvac_b has preheat system
    preheat_system = hvac_b.get("preheat_system")
    is_hvac_sys_preheat_fluid_loop_purchased_heating_flag = (
        preheat_system is not None
        and preheat_system.get("hot_water_loop") in purchased_heating_loop_list_b
    )

    return is_hvac_sys_preheat_fluid_loop_purchased_heating_flag
