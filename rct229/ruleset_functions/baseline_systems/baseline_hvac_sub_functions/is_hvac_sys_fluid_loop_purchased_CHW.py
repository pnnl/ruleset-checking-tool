from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

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
    is_hvac_sys_fluid_loop_purchased_chw_flag = False
    purchased_cooling_loop_list_b = []

    external_fluid_sources = rmi_b.get("external_fluid_source")
    if external_fluid_sources:
        for external_fluid_source in external_fluid_sources:
            if external_fluid_source.get("type") == EXTERNAL_FLUID_SOURCE.CHILLED_WATER and external_fluid_source.get("loop") is not None:
                purchased_cooling_loop_list_b.append(external_fluid_source["loop"])

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
        "id",
        hvac_b_id,
        rmi_b,
    )
    # Check if hvac_b has preheat system
    cooling_system = hvac_b.get("cooling_system")
    is_hvac_sys_fluid_loop_purchased_chw_flag = (
        cooling_system is not None
        and cooling_system.get("chilled_water_loop") in purchased_cooling_loop_list_b
    )

    return is_hvac_sys_fluid_loop_purchased_chw_flag
