from rct229.data.schema_enums import schema_enums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

FLUID_LOOP_TYPE = schema_enums["FluidLoopOptions"]


def are_all_terminal_heating_loops_attached_to_boiler(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is attached to a boiler. Returns FALSE if this is not the case.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs

    Returns
    -------
    bool
        True: fluid loop associated with the heating_from_loop associated with each terminal unit is attached to a boiler
        False: otherwise
    """
    are_all_terminal_heating_loops_attached_to_boiler_flag = True
    boilers = find_all("$.boilers[*]", rmi_b)
    loop_boiler_dict = dict()
    for boiler_b in boilers:
        loop_id = getattr_(boiler_b, "boiler", "loop")
        if not loop_id in loop_boiler_dict.keys():
            loop_boiler_dict[loop_id] = []
        loop_boiler_dict[loop_id].append(boiler_b)

    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_with_field_value(
            "$.buildings[*].building_segments[*].zones[*].terminals",
            "id",
            terminal_b_id,
            rmi_b,
        )
        heating_from_loop = terminal_b.get("heating_from_loop")
        if heating_from_loop:
            fluid_loop = find_exactly_one_with_field_value(
                "$.fluid_loops",
                "id",
                heating_from_loop,
                rmi_b,
            )
            if (
                getattr_(fluid_loop, "fluid loop", "type") != FLUID_LOOP_TYPE.HEATING
                or heating_from_loop not in loop_boiler_dict.keys()
            ):
                are_all_terminal_heating_loops_attached_to_boiler_flag = False
                break
        else:
            are_all_terminal_heating_loops_attached_to_boiler_flag = False

    return are_all_terminal_heating_loops_attached_to_boiler_flag
