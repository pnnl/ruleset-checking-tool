from rct229.data.schema_enums import schema_enums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value, find_all

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]
FLUID_LOOP_TYPE = schema_enums["FluidLoopOptions"]


def are_all_terminal_heating_loops_purchased_heating(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is purchased heating. Returns FALSE if this is not the case.
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs
    Returns
    -------
    bool
        True: fluid loop associated with the heating_from_loop associated with each terminal unit is purchased heating
        False: otherwise
    """
    are_all_terminal_heating_loops_purchased_heating_flag = True
    purchased_heating_loop_id_list_b = []

    # external_fluid_sources = rmi_b.get("external_fluid_source")
    purchased_heating_loop_id_list_b = [
        *find_all(
            f"(external_fluid_source[?(@.type=={EXTERNAL_FLUID_SOURCE.HOT_WATER})].loop) | (external_fluid_source[?("
            f"@.type=={EXTERNAL_FLUID_SOURCE.STEAM})].loop)",
            rmi_b,
        )
    ]

    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_with_field_value(
            "$.buildings[*].building_segments[*].zones[*].terminals",
            "id",
            terminal_b_id,
            rmi_b,
        )
        heating_from_loop_id = terminal_b.get("heating_from_loop")
        if heating_from_loop_id:
            fluid_loop = find_exactly_one_with_field_value(
                "$.fluid_loops",
                "id",
                heating_from_loop_id,
                rmi_b,
            )
            if (
                getattr_(fluid_loop, "fluid loop", "type") != FLUID_LOOP_TYPE.HEATING
                or heating_from_loop_id not in purchased_heating_loop_id_list_b
            ):
                are_all_terminal_heating_loops_purchased_heating_flag = False
                break
        else:
            are_all_terminal_heating_loops_purchased_heating_flag = False
            break

    return are_all_terminal_heating_loops_purchased_heating_flag
