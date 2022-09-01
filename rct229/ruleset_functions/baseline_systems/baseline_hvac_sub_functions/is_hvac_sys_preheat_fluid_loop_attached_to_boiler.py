from rct229.data.schema_enums import schema_enums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one_with_field_value, find_exactly_one_with_field_value

FLUID_LOOP = schema_enums["FluidLoopOptions"]


def is_hvac_sys_preheat_fluid_loop_attached_to_boiler(rmi_b, hvac_b_id):
    """Returns True if the fluid loop associated with preheat system associated with the HVAC system is attached to a boiler.
    Returns False if this is not the case.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: preheat system is attached to a boiler
        False: otherwise
    """
    is_hvac_sys_preheat_fluid_loop_attached_to_boiler_flag = False
    boilers = find_all("$.boilers[*]", rmi_b)
    loop_boiler_dict = dict()
    for boiler_b in boilers:
        loop_id = getattr_(boiler_b, "boiler", "loop")
        if not loop_id in loop_boiler_dict.keys():
            loop_boiler_dict[loop_id] = []
        loop_boiler_dict[loop_id].append(boiler_b)

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value (
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
        "id",
        hvac_b_id,
        rmi_b,
    )
    # Check if hvac_b has preheat system
    preheat_system = hvac_b.get("preheat_system")
    if preheat_system:
        hot_water_loop_id = preheat_system.get("hot_water_loop")
        # Check if the preheat system has hot water loop and the hot water loop connects to a boiler(s)
        if hot_water_loop_id and hot_water_loop_id in loop_boiler_dict.keys():
            hot_water_loop = find_one_with_field_value(
                "$.fluid_loops", "id", hot_water_loop_id, rmi_b
            )
            # check if the boiler-preheat system loop type is Heating
            if (
                hot_water_loop
                and getattr_(hot_water_loop, "fluidloop", "type") == FLUID_LOOP.HEATING
            ):
                is_hvac_sys_preheat_fluid_loop_attached_to_boiler_flag = True

    return is_hvac_sys_preheat_fluid_loop_attached_to_boiler_flag
