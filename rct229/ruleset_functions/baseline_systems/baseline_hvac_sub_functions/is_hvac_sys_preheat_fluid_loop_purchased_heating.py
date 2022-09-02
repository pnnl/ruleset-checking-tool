from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]


def is_hvac_sys_preheat_fluid_loop_purchased_heating(rmi_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the preheating system associated with the HVAC system is
    attached to an external purchased heating loop. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: fluid loop associated with the preheating system associated with the HVAC system is attached to an external purchased heating loop
        False: otherwise
    """
    is_hvac_sys_preheat_fluid_loop_purchased_heating_flag = False
    purchased_heating_loop_list_b = []

    external_fluid_sources = rmi_b.get("external_fluid_source")
    if external_fluid_sources:
        for external_fluid_source in external_fluid_sources:
            if external_fluid_source.get("type") in [
                EXTERNAL_FLUID_SOURCE.HOT_WATER,
                EXTERNAL_FLUID_SOURCE.STEAM,
            ]:
                purchased_heating_loop_list_b.append(external_fluid_source["id"])

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
        "id",
        hvac_b_id,
        rmi_b,
    )
    # Check if hvac_b has preheat system
    if hvac_b.get("preheat_system") and hvac_b["preheat_system"].get("hot_water_loop"):
        fluid_loop_b_id = hvac_b["preheat_system"]["hot_water_loop"]
        if fluid_loop_b_id in purchased_heating_loop_list_b:
            is_hvac_sys_preheat_fluid_loop_purchased_heating_flag = True

    return is_hvac_sys_preheat_fluid_loop_purchased_heating_flag
