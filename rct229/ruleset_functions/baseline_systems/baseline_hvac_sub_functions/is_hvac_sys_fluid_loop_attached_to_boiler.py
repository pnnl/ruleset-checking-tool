from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import (
    find_all,
    find_exactly_one_with_field_value,
    find_one,
)

FLUID_LOOP = schema_enums["FluidLoopOptions"]


def is_hvac_sys_fluid_loop_attached_to_boiler(rmi_b, hvac_b_id):
    """Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler
        False: otherwise
    """
    is_hvac_sys_fluid_loop_attached_to_boiler_flag = False
    boiler_loop_ids = find_all("$.boilers[*].loop", rmi_b)
    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems[*]",
        "id",
        hvac_b_id,
        rmi_b,
    )
    hot_water_loop_id = find_one("heating_system.hot_water_loop", hvac_b)
    if hot_water_loop_id in boiler_loop_ids:
        hot_water_loop = find_exactly_one_with_field_value(
            "$.fluid_loops[*]", "id", hot_water_loop_id, rmi_b
        )
        is_hvac_sys_fluid_loop_attached_to_boiler_flag = (
            find_one("type", hot_water_loop) == FLUID_LOOP.HEATING
        )

    return is_hvac_sys_fluid_loop_attached_to_boiler_flag
