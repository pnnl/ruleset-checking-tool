from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_chw_loops_purcahsed_cooling import (
    are_all_terminal_chw_loops_purchased_cooling,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_chilled_water import (
    are_all_terminal_cool_sources_chilled_water,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_CAV_with_none_equal_to_null import (
    are_all_terminal_types_cav_with_none_equal_to_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.do_all_terminals_have_one_fan import (
    do_all_terminals_have_one_fan,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_none import (
    is_hvac_sys_cooling_type_none,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import (
    has_fan_system,
    has_heating_system,
    has_preheat_system,
)

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_baseline_system_1_c(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Returns true or false to whether the baseline system type is 1c (system 1 with purchased CHW and purchased HW).

    Parameters
    ----------
    rmi_b JSON, To evaluate if the hvac system is modeled as either Sys-1c in the B_RMD.

    hvac_b_id String, The id of the hvac system to evaluate.

    terminal_unit_id_list List<String>, list of terminal unit IDs associated with the HVAC system to be evaluated.
    These are sent to this function from the is_baseline_system_1 function.

    zone_id_list  List<String>, list of zone IDs associated with the HVAC system to be evaluated. TThese are sent to
    this function from the is_baseline_system_1 function.

    Returns true or false to whether the baseline system type is 1c (system 1 with purchased CHW and purchased HW).
     -------
    """

    # check if the hvac system has the required sub systems for system type 1 c
    # if preheat, heating, and fan systems DON'T exist, has_required_sys=True, else, False
    has_required_sys = not (
        has_preheat_system(rmi_b, hvac_b_id)
        and has_heating_system(rmi_b, hvac_b_id)
        and has_fan_system(rmi_b, hvac_b_id)
    )

    return (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_cooling_type_none(rmi_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_heat_sources_hot_water(rmi_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_chilled_water(rmi_b, terminal_unit_id_list)
        and do_all_terminals_have_one_fan(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_cav_with_none_equal_to_null(
            rmi_b, terminal_unit_id_list
        )
        and are_all_terminal_heating_loops_purchased_heating(
            rmi_b, terminal_unit_id_list
        )
        and are_all_terminal_chw_loops_purchased_cooling(rmi_b, terminal_unit_id_list)
    )
