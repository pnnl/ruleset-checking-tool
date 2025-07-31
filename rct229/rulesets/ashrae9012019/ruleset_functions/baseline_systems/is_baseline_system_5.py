from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fans_null import (
    are_all_terminal_fans_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_attached_to_boiler import (
    are_all_terminal_heating_loops_attached_to_boiler,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_attached_to_boiler import (
    is_hvac_sys_preheat_fluid_loop_attached_to_boiler,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_purchased_heating import (
    is_hvac_sys_preheat_fluid_loop_purchased_heating,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import (
    has_cooling_system,
    has_heating_system,
    has_preheat_system,
)

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = SchemaEnums.schema_enums["CoolingSystemOptions"]


def is_baseline_system_5(rmd_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
     Get either Sys-5, Sys-5b, or Not_Sys_5 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 5 (Package VAV with Reheat) or system 5b (system 5 with purchased heating).

     Parameters
     ----------
     rmd_b json
         To evaluate if the hvac system is modeled as either Sys-5, Sys-5b, or Not_Sys_5 in the B_RMD.
     hvac_b_id list
         The id of the hvac system to evaluate.
     terminal_unit_id_list
         List list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
     zone_id_list list
         list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

    Returns
     -------
     The function returns either Sys-5, Sys-5b, or Not_Sys_5 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 5 (Package VAV with Reheat) or system 5b (system 5 with purchased heating).
    """

    is_baseline_system_5 = HVAC_SYS.UNMATCHED

    # check if the hvac system has the required sub systems for system type 5
    # if heating system DOESN'T exist and preheat/cooling systems exist,  has_required_sys=True, else, False
    has_required_sys = (
        has_preheat_system(rmd_b, hvac_b_id)
        and not has_heating_system(rmd_b, hvac_b_id)
        and has_cooling_system(rmd_b, hvac_b_id)
    )

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_preheating_type_fluid_loop(rmd_b, hvac_b_id)
        and is_hvac_sys_cooling_type_dx(rmd_b, hvac_b_id)
        and is_hvac_sys_fan_sys_vsd(rmd_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmd_b, zone_id_list)
        and are_all_terminal_heat_sources_hot_water(rmd_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmd_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmd_b, terminal_unit_id_list)
        and are_all_terminal_types_VAV(rmd_b, terminal_unit_id_list)
    )
    if are_sys_data_matched:
        if is_hvac_sys_preheat_fluid_loop_attached_to_boiler(
            rmd_b, hvac_b_id
        ) and are_all_terminal_heating_loops_attached_to_boiler(
            rmd_b, terminal_unit_id_list
        ):
            is_baseline_system_5 = HVAC_SYS.SYS_5
        elif is_hvac_sys_preheat_fluid_loop_purchased_heating(
            rmd_b, hvac_b_id
        ) and are_all_terminal_heating_loops_purchased_heating(
            rmd_b, terminal_unit_id_list
        ):
            is_baseline_system_5 = HVAC_SYS.SYS_5B

    return is_baseline_system_5
