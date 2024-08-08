from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

EXTERNAL_FLUID_SOURCE = SchemaEnums.schema_enums["ExternalFluidSourceOptions"]


def is_hvac_sys_fluid_loop_purchased_heating(rmd_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop
        False: otherwise
    """
    # Get a list of loop ids in external fluid sources whose type are either hot water or steam
    purchased_heating_loop_id_list_b = find_all(
        f'$.external_fluid_sources[*][?(@.type="{EXTERNAL_FLUID_SOURCE.HOT_WATER}"), ?(@.type="{EXTERNAL_FLUID_SOURCE.STEAM}")].loop',
        rmd_b,
    )

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)

    # the hvac_sys has a heating system and the heating system has a hot_water_loop and
    # the loop id is in the purchased_heating_loop_id_list
    is_hvac_sys_fluid_loop_purchased_heating_flag = (
        find_one("heating_system.hot_water_loop", hvac_b)
        in purchased_heating_loop_id_list_b
    )

    return is_hvac_sys_fluid_loop_purchased_heating_flag
