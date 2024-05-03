from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_chw_loops_purcahsed_cooling import (
    are_all_terminal_chw_loops_purchased_cooling,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_chilled_water import (
    are_all_terminal_cool_sources_chilled_water,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_attached_to_boiler import (
    are_all_terminal_heating_loops_attached_to_boiler,
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


def is_baseline_system_1_a(rmd_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Returns true or false to whether the baseline system type is 1a (system 1 with purchased CHW and HW served by a boiler).

    Parameters
    ----------
    rmd_b JSON, To evaluate if the hvac system is modeled as either Sys-1c in the B_RMD.

    hvac_b_id String, The id of the hvac system to evaluate.

    terminal_unit_id_list List<String>, list of terminal unit IDs associated with the HVAC system to be evaluated.
    These are sent to this function from the is_baseline_system_1 function.

    zone_id_list  List<String>, list of zone IDs associated with the HVAC system to be evaluated. TThese are sent to
    this function from the is_baseline_system_1 function.

    Returns true or false to whether the baseline system type is 1a (system 1 with purchased CHW and HW served by a boiler).
     -------
    """

    # check if the hvac system has the required sub systems for system type 1 a
    # if preheat, heating, and fan systems DON'T exist, has_required_sys=True, else, False
    has_required_sys = not (
        has_preheat_system(rmd_b, hvac_b_id)
        and has_heating_system(rmd_b, hvac_b_id)
        and has_fan_system(rmd_b, hvac_b_id)
    )

    return (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_cooling_type_none(rmd_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmd_b, zone_id_list)
        and are_all_terminal_heat_sources_hot_water(rmd_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_chilled_water(rmd_b, terminal_unit_id_list)
        and do_all_terminals_have_one_fan(rmd_b, terminal_unit_id_list)
        and are_all_terminal_types_cav_with_none_equal_to_null(
            rmd_b, terminal_unit_id_list
        )
        and are_all_terminal_heating_loops_attached_to_boiler(
            rmd_b, terminal_unit_id_list
        )
        and are_all_terminal_chw_loops_purchased_cooling(rmd_b, terminal_unit_id_list)
    )
