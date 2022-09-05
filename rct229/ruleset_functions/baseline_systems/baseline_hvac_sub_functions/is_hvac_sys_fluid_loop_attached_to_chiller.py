from rct229.data.schema_enums import schema_enums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import (
    find_all,
    find_exactly_one_with_field_value,
    find_one_with_field_value,
)

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
    loop_chiller_dict = dict()
    for chiller_b in chillers:
        loop_id = getattr_(chiller_b, "chiller", "cooling_loop")
        if not loop_id in loop_chiller_dict.keys():
            loop_chiller_dict[loop_id] = []
        loop_chiller_dict[loop_id].append(chiller_b)

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
        "id",
        hvac_b_id,
        rmi_b,
    )
    # Check if hvac_b has preheat system
    cooling_system = hvac_b.get("cooling_system")
    if cooling_system:
        chilled_water_loop_id = cooling_system.get("chilled_water_loop")
        # Check if the cooling system has chilled water loop and the chilled water loop connects to a chiller(s)
        if chilled_water_loop_id and chilled_water_loop_id in loop_chiller_dict.keys():
            chilled_water_loop = find_one_with_field_value(
                "$.fluid_loops", "id", chilled_water_loop_id, rmi_b
            )
            # check if the chiller system loop type is Cooling
            if (
                chilled_water_loop
                and getattr_(chilled_water_loop, "fluidloop", "type")
                == FLUID_LOOP.COOLING
            ):
                is_hvac_sys_fluid_loop_attached_to_chiller_flag = True
    return is_hvac_sys_fluid_loop_attached_to_chiller_flag
