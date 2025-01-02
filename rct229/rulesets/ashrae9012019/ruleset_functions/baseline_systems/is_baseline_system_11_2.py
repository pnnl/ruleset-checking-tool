from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fans_null import (
    are_all_terminal_fans_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_none_or_null import (
    are_all_terminal_heat_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_hvac_system_serve_single_zone import (
    does_hvac_system_serve_single_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_boiler import (
    is_hvac_sys_fluid_loop_attached_to_boiler,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_CHW import (
    is_hvac_sys_fluid_loop_purchased_chw,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import has_preheat_system

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_baseline_system_11_2(rmd_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-11.2, Sys-11.2a or Not_Sys_11.2 string output which indicates whether the HVAC system is ASHRAE
    90.1 2019 Appendix G system 11.2 (Single Zone VAV System with Hot Water Heating (Boiler)) or system 11.2a (system
    11.2 with purchased CHW).

    Parameters
    ----------
    rmd_b: json To evaluate if the hvac system is modeled as either Sys-11.2, Sys-11.2a or Not_Sys_11.2 in the B_rmd.
    hvac_b_id: String, The id of the hvac system to evaluate.
    terminal_unit_id_list: List<String>, list of terminal unit IDs associated with the HVAC system to be evaluated. These are
                            sent to this function from the master get_baseline_system_types function.
    zone_id_list: List<String>, list of zone IDs associated with the HVAC system to be evaluated. These are sent to this
                        function from the master get_baseline_system_types function.

    Returns string The function returns either Sys-11.2, Sys-11.2a or Not_Sys string output which indicates
    whether the HVAC system is ASHRAE 90.1 2019 Appendix G 11.2 (Single Zone VAV System with Hot Water Heating (
    Boiler)) or system 11.2a (system 11.2 with purchased CHW). -------
    """
    is_baseline_system_11_2_str = HVAC_SYS.UNMATCHED

    # check if the hvac system has the required sub systems for system type 11.2
    # if preheat system DOESN'T exist, has_required_sys=True, else, False
    has_required_sys = not has_preheat_system(rmd_b, hvac_b_id)

    are_sys_data_matched = (
        has_required_sys
        and is_hvac_sys_cooling_type_fluid_loop(rmd_b, hvac_b_id)
        and is_hvac_sys_fan_sys_vsd(rmd_b, hvac_b_id)
        and does_hvac_system_serve_single_zone(rmd_b, zone_id_list)
        and does_each_zone_have_only_one_terminal(rmd_b, zone_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmd_b, terminal_unit_id_list)
        and are_all_terminal_heat_sources_none_or_null(rmd_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmd_b, terminal_unit_id_list)
        and are_all_terminal_types_VAV(rmd_b, terminal_unit_id_list)
    )

    if are_sys_data_matched and is_hvac_sys_fluid_loop_attached_to_boiler(
        rmd_b, hvac_b_id
    ):
        if is_hvac_sys_fluid_loop_attached_to_chiller(rmd_b, hvac_b_id):
            is_baseline_system_11_2_str = HVAC_SYS.SYS_11_2
        elif is_hvac_sys_fluid_loop_purchased_chw(rmd_b, hvac_b_id):
            is_baseline_system_11_2_str = HVAC_SYS.SYS_11_2A

    return is_baseline_system_11_2_str
