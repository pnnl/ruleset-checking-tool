from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import (
    find_all,
    find_exactly_one_with_field_value,
    find_one,
)

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]


def is_hvac_sys_fluid_loop_purchased_heating(rmi_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop
        False: otherwise
    """
    purchased_heating_loop_id_list_b = [
        *find_all(
            f"(external_fluid_source[?(@.type=={EXTERNAL_FLUID_SOURCE.HOT_WATER})].loop) | (external_fluid_source[?(@.type=={EXTERNAL_FLUID_SOURCE.STEAM})].loop)",
            rmi_b,
        )
    ]

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
        "id",
        hvac_b_id,
        rmi_b,
    )

    # the hvac_sys has a heating system and the heating system has a hot_water_loop and
    # the loop id is in the purchased_heating_loop_id_list
    is_hvac_sys_fluid_loop_purchased_heating_flag = (
        find_one("heating_system.hot_water_loop", hvac_b)
        in purchased_heating_loop_id_list_b
    )

    return is_hvac_sys_fluid_loop_purchased_heating_flag
