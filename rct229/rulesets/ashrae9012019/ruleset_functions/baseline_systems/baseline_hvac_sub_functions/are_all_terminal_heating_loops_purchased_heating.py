from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import (
    find_exactly_one_fluid_loop,
    find_exactly_one_terminal_unit,
)

EXTERNAL_FLUID_SOURCE = SchemaEnums.schema_enums["ExternalFluidSourceOptions"]
FLUID_LOOP_TYPE = SchemaEnums.schema_enums["FluidLoopOptions"]


def are_all_terminal_heating_loops_purchased_heating(rmd_b, terminal_unit_id_list):
    """Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is purchased heating. Returns FALSE if this is not the case.
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
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
            f'external_fluid_sources[*][?(@.type="{EXTERNAL_FLUID_SOURCE.HOT_WATER}"), ?(@.type="{EXTERNAL_FLUID_SOURCE.STEAM}")].loop',
            rmd_b,
        )
    ]

    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmd_b, terminal_b_id)
        heating_from_loop_id = terminal_b.get("heating_from_loop")
        if (
            are_all_terminal_heating_loops_purchased_heating_flag
            and heating_from_loop_id
        ):
            fluid_loop = find_exactly_one_fluid_loop(rmd_b, heating_from_loop_id)
            if (
                getattr_(fluid_loop, "fluid loop", "type") != FLUID_LOOP_TYPE.HEATING
                or heating_from_loop_id not in purchased_heating_loop_id_list_b
            ):
                are_all_terminal_heating_loops_purchased_heating_flag = False
        else:
            are_all_terminal_heating_loops_purchased_heating_flag = False

    return are_all_terminal_heating_loops_purchased_heating_flag
