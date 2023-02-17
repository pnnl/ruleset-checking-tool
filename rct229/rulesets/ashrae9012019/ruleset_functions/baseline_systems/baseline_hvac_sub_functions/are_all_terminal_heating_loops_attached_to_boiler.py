from rct229.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_fluid_loop,
    find_exactly_one_terminal_unit,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one

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
    loop_boiler_id_list = [
        getattr_(boiler_b, "boiler", "loop")
        for boiler_b in find_all("$.boilers[*]", rmi_b)
    ]

    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmi_b, terminal_b_id)
        heating_from_loop_id = terminal_b.get("heating_from_loop")
        # cond 1 allows heating_from_loop_id to be None, cond 2 allows fluid_loop to be None.
        if (
            heating_from_loop_id not in loop_boiler_id_list
            # return None if terminal_b has no heating_from_loop field, or
            # the heating_from_loop id cannot be found in fluid_loops
            or find_one(
                "type", find_exactly_one_fluid_loop(rmi_b, heating_from_loop_id)
            )
            != FLUID_LOOP_TYPE.HEATING
        ):
            are_all_terminal_heating_loops_attached_to_boiler_flag = False
            break

    return are_all_terminal_heating_loops_attached_to_boiler_flag
