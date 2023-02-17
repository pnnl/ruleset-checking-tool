from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_fluid_loop,
    find_exactly_one_terminal_unit,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

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

    # get the list of loop ids if the external fluid source matches to either hot water or steam
    purchased_heating_loop_id_list_b = [
        *find_all(
            f'external_fluid_source[*][?(@.type="{EXTERNAL_FLUID_SOURCE.HOT_WATER}"), ?(@.type="{EXTERNAL_FLUID_SOURCE.STEAM}")].loop',
            rmi_b,
        )
    ]

    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmi_b, terminal_b_id)
        heating_from_loop_id = terminal_b.get("heating_from_loop")
        if heating_from_loop_id:
            fluid_loop = find_exactly_one_fluid_loop(rmi_b, heating_from_loop_id)
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
