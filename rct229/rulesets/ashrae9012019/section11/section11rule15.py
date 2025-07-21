from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all
from pydash import curry

MANUAL_CHECK_REQUIRED_MSG = (
    "Proposed Service Water Heating Use is less than the baseline. "
    "Manually verify that reduction is due to an ECM that reduces service water heating use, such as low-flow fixtures."
)

# get either - success will get the data, failed will return default value
getEither = curry(lambda o, k: o.get(k) if isinstance(o, dict) else None)


class PRM9012019Rule06k20(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule06k20, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule06k20.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-15",
            description=(
                "Service water loads and use shall be the same for both the proposed design and baseline building design.Exceptions:"
                "(1) Energy Efficiency Measures approved by the Authority Having Jurisdiction are used in the proposed model "
                "(2) SWH energy consumption can be demonstrated to be reduced by reducing the required temperature of service mixed water, by increasing the temperature, or by increasing the temperature of the entering makeup water."
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, (g)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule06k20.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule06k20.RMDRule.SWHUseRule(),
                index_rmd=BASELINE_0,
                # TODO, change the path if the service_water_heating_uses moved to building_segment level
                list_path="$.service_water_heating_uses[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            swh_use_ids = []
            for building_segment_b in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                swh_use_list_b = get_swh_uses_associated_with_each_building_segment(
                    rmd_b
                )[building_segment_b["id"]]
                swh_use_ids += [
                    swh_use_b["id"]
                    for swh_use_b in swh_use_list_b
                    if swh_use_b["id"] not in swh_use_ids
                ]

            for building_segment_p in find_all(
                "$.buildings[*].building_segments[*]", rmd_p
            ):
                swh_use_list_p = get_swh_uses_associated_with_each_building_segment(
                    rmd_p
                )[building_segment_p["id"]]
                swh_use_ids += [
                    swh_use_p["id"]
                    for swh_use_p in swh_use_list_p
                    if swh_use_p["id"] not in swh_use_ids
                ]

            return len(set(swh_use_ids)) > 0

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            swh_dist_sys_dict_b = {}
            swh_dist_sys_dict_p = {}

            for swh_dist_sys_b in find_all(
                "$.service_water_heating_distribution_systems[*]",
                rmd_b,
            ):
                swh_dist_sys_dict_b[swh_dist_sys_b["id"]] = swh_dist_sys_b

            for swh_dist_sys_p in find_all(
                "$.service_water_heating_distribution_systems[*]",
                rmd_p,
            ):
                swh_dist_sys_dict_p[swh_dist_sys_p["id"]] = swh_dist_sys_p

            return {
                "swh_dist_sys_dict_b": swh_dist_sys_dict_b,
                "swh_dist_sys_dict_p": swh_dist_sys_dict_p,
            }

        class SWHUseRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule06k20.RMDRule.SWHUseRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                )

            def get_calc_vals(self, context, data=None):
                # the swh_use object type can be dict or None
                swh_use_b = context.BASELINE_0
                swh_use_p = context.PROPOSED

                # curry function that help to extract the data from swh_use object
                get_swh_use_b = getEither(swh_use_b)
                get_swh_use_p = getEither(swh_use_p)

                swh_use_id_b = get_swh_use_b("id")
                swh_use_id_p = get_swh_use_p("id")

                swh_dist_sys_dict_b = data["swh_dist_sys_dict_b"]
                swh_dist_sys_dict_p = data["swh_dist_sys_dict_p"]

                swh_use_served_by_distribution_system_id_b = get_swh_use_b(
                    "served_by_distribution_system"
                )
                swh_use_served_by_distribution_system_id_p = get_swh_use_p(
                    "served_by_distribution_system"
                )

                swh_use_served_by_distribution_system_b = (
                    swh_dist_sys_dict_b[swh_use_served_by_distribution_system_id_b]
                    if swh_use_served_by_distribution_system_id_b
                    else None
                )

                swh_use_served_by_distribution_system_p = (
                    swh_dist_sys_dict_p[swh_use_served_by_distribution_system_id_p]
                    if swh_use_served_by_distribution_system_id_p
                    else None
                )

                # Curry function to extract data from distribution system object
                get_swh_dist_sys_b = getEither(swh_use_served_by_distribution_system_b)
                get_swh_dist_sys_p = getEither(swh_use_served_by_distribution_system_p)

                swh_use_design_supply_water_temperature_b = get_swh_dist_sys_b(
                    "design_supply_water_temperature"
                )
                swh_use_design_supply_water_temperature_p = get_swh_dist_sys_p(
                    "design_supply_water_temperature"
                )

                return {
                    "is_swh_use_none_b": swh_use_b is None,
                    "is_swh_use_none_p": swh_use_p is None,
                    "swh_use_b": get_swh_use_b("use"),
                    "swh_use_p": get_swh_use_p("use"),
                    "swh_use_id_b": swh_use_id_b,
                    "swh_use_id_p": swh_use_id_p,
                    "swh_use_use_units_b": get_swh_use_b("use_units"),
                    "swh_use_use_units_p": swh_use_p.get("use_units"),
                    "swh_use_multiplier_schedule_b": get_swh_use_b(
                        "use_multiplier_schedule"
                    ),
                    "swh_use_multiplier_schedule_p": get_swh_use_p(
                        "use_multiplier_schedule"
                    ),
                    "swh_use_temperature_at_fixture_b": get_swh_use_b(
                        "temperature_at_fixture"
                    ),
                    "swh_use_temperature_at_fixture_p": get_swh_use_p(
                        "temperature_at_fixture"
                    ),
                    "swh_use_water_mains_temperature_schedule_b": get_swh_use_b(
                        "entering_water_mains_temperature_schedule"
                    ),
                    "swh_use_water_mains_temperature_schedule_p": get_swh_use_p(
                        "entering_water_mains_temperature_schedule"
                    ),
                    "swh_use_served_by_distribution_system_b": swh_use_served_by_distribution_system_b,
                    "swh_use_served_by_distribution_system_p": swh_use_served_by_distribution_system_p,
                    "swh_use_design_supply_water_temperature_b": swh_use_design_supply_water_temperature_b,
                    "swh_use_design_supply_water_temperature_p": swh_use_design_supply_water_temperature_p,
                    "is_heat_recovered_by_drain_b": get_swh_use_b(
                        "is_heat_recovered_by_drain"
                    ),
                    "is_heat_recovered_by_drain_p": get_swh_use_p(
                        "is_heat_recovered_by_drain"
                    ),
                    "is_recovered_heat_used_by_cold_side_feed_b": get_swh_use_b(
                        "is_recovered_heat_used_by_cold_side_feed"
                    ),
                    "is_recovered_heat_used_by_cold_side_feed_p": get_swh_use_p(
                        "is_recovered_heat_used_by_cold_side_feed"
                    ),
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                swh_use_b = calc_vals["swh_use_b"] if calc_vals["swh_use_b"] else 0.0
                swh_use_p = calc_vals["swh_use_p"] if calc_vals["swh_use_p"] else 0.0

                is_swh_use_none_b = calc_vals["is_swh_use_none_b"]
                is_swh_use_none_p = calc_vals["is_swh_use_none_p"]

                swh_use_use_units_b = calc_vals["swh_use_use_units_b"]
                swh_use_use_units_p = calc_vals["swh_use_use_units_p"]

                swh_use_multiplier_schedule_b = calc_vals[
                    "swh_use_multiplier_schedule_b"
                ]
                swh_use_multiplier_schedule_p = calc_vals[
                    "swh_use_multiplier_schedule_p"
                ]
                swh_use_temperature_at_fixture_b = calc_vals[
                    "swh_use_temperature_at_fixture_b"
                ]
                swh_use_temperature_at_fixture_p = calc_vals[
                    "swh_use_temperature_at_fixture_p"
                ]
                swh_use_water_mains_temperature_schedule_b = calc_vals[
                    "swh_use_water_mains_temperature_schedule_b"
                ]
                swh_use_water_mains_temperature_schedule_p = calc_vals[
                    "swh_use_water_mains_temperature_schedule_p"
                ]
                swh_use_served_by_distribution_system_b = calc_vals[
                    "swh_use_served_by_distribution_system_b"
                ]
                swh_use_served_by_distribution_system_p = calc_vals[
                    "swh_use_served_by_distribution_system_p"
                ]
                swh_use_design_supply_water_temperature_b = calc_vals[
                    "swh_use_design_supply_water_temperature_b"
                ]
                swh_use_design_supply_water_temperature_p = calc_vals[
                    "swh_use_design_supply_water_temperature_p"
                ]
                is_heat_recovered_by_drain_b = calc_vals["is_heat_recovered_by_drain_b"]
                is_heat_recovered_by_drain_p = calc_vals["is_heat_recovered_by_drain_p"]
                is_recovered_heat_used_by_cold_side_feed_b = calc_vals[
                    "is_recovered_heat_used_by_cold_side_feed_b"
                ]
                is_recovered_heat_used_by_cold_side_feed_p = calc_vals[
                    "is_recovered_heat_used_by_cold_side_feed_p"
                ]

                return (
                    is_swh_use_none_b == is_swh_use_none_p
                    and swh_use_use_units_b == swh_use_use_units_p
                    and swh_use_multiplier_schedule_b == swh_use_multiplier_schedule_p
                    and swh_use_temperature_at_fixture_b
                    == swh_use_temperature_at_fixture_p
                    and swh_use_water_mains_temperature_schedule_b
                    == swh_use_water_mains_temperature_schedule_p
                    and swh_use_served_by_distribution_system_b
                    == swh_use_served_by_distribution_system_p
                    and swh_use_design_supply_water_temperature_b
                    == swh_use_design_supply_water_temperature_p
                    and is_heat_recovered_by_drain_b == is_heat_recovered_by_drain_p
                    and is_recovered_heat_used_by_cold_side_feed_b
                    == is_recovered_heat_used_by_cold_side_feed_p
                    and swh_use_b > swh_use_p
                )

            def rule_check(self, context, calc_vals=None, data=None):
                # it is for sure that this is either scenario which means there is no None.
                swh_use_b = calc_vals["swh_use_b"] if calc_vals["swh_use_b"] else 0.0
                swh_use_p = calc_vals["swh_use_p"] if calc_vals["swh_use_p"] else 0.0

                is_swh_use_none_b = calc_vals["is_swh_use_none_b"]
                is_swh_use_none_p = calc_vals["is_swh_use_none_p"]

                swh_use_use_units_b = calc_vals["swh_use_use_units_b"]
                swh_use_use_units_p = calc_vals["swh_use_use_units_p"]

                swh_use_multiplier_schedule_b = calc_vals[
                    "swh_use_multiplier_schedule_b"
                ]
                swh_use_multiplier_schedule_p = calc_vals[
                    "swh_use_multiplier_schedule_p"
                ]
                swh_use_temperature_at_fixture_b = calc_vals[
                    "swh_use_temperature_at_fixture_b"
                ]
                swh_use_temperature_at_fixture_p = calc_vals[
                    "swh_use_temperature_at_fixture_p"
                ]
                swh_use_water_mains_temperature_schedule_b = calc_vals[
                    "swh_use_water_mains_temperature_schedule_b"
                ]
                swh_use_water_mains_temperature_schedule_p = calc_vals[
                    "swh_use_water_mains_temperature_schedule_p"
                ]
                swh_use_served_by_distribution_system_b = calc_vals[
                    "swh_use_served_by_distribution_system_b"
                ]
                swh_use_served_by_distribution_system_p = calc_vals[
                    "swh_use_served_by_distribution_system_p"
                ]
                swh_use_design_supply_water_temperature_b = calc_vals[
                    "swh_use_design_supply_water_temperature_b"
                ]
                swh_use_design_supply_water_temperature_p = calc_vals[
                    "swh_use_design_supply_water_temperature_p"
                ]
                is_heat_recovered_by_drain_b = calc_vals["is_heat_recovered_by_drain_b"]
                is_heat_recovered_by_drain_p = calc_vals["is_heat_recovered_by_drain_p"]
                is_recovered_heat_used_by_cold_side_feed_b = calc_vals[
                    "is_recovered_heat_used_by_cold_side_feed_b"
                ]
                is_recovered_heat_used_by_cold_side_feed_p = calc_vals[
                    "is_recovered_heat_used_by_cold_side_feed_p"
                ]

                rule_result = True
                if (not is_swh_use_none_b and is_swh_use_none_p) or (
                    is_swh_use_none_b and not is_swh_use_none_p
                ):
                    rule_result = False
                else:
                    if swh_use_use_units_b != swh_use_use_units_p:
                        rule_result = False

                    if swh_use_multiplier_schedule_b != swh_use_multiplier_schedule_p:
                        rule_result = False
                    if (
                        swh_use_temperature_at_fixture_b
                        != swh_use_temperature_at_fixture_p
                    ):
                        rule_result = False
                    if (
                        swh_use_water_mains_temperature_schedule_b
                        != swh_use_water_mains_temperature_schedule_p
                    ):
                        rule_result = False
                    if is_heat_recovered_by_drain_b != is_heat_recovered_by_drain_p:
                        rule_result = False
                    if (
                        is_recovered_heat_used_by_cold_side_feed_b
                        != is_recovered_heat_used_by_cold_side_feed_p
                    ):
                        rule_result = False
                    if (
                        swh_use_served_by_distribution_system_b
                        != swh_use_served_by_distribution_system_p
                    ):
                        rule_result = False
                    if (
                        swh_use_design_supply_water_temperature_b
                        != swh_use_design_supply_water_temperature_p
                    ):
                        rule_result = False
                    if swh_use_b < swh_use_p:
                        rule_result = False

                return rule_result

            def get_fail_msg(self, context, calc_vals=None, data=None):
                swh_use_b = calc_vals["swh_use_b"] if calc_vals["swh_use_b"] else 0.0
                swh_use_p = calc_vals["swh_use_p"] if calc_vals["swh_use_p"] else 0.0

                swh_use_id_b = calc_vals["swh_use_id_b"]
                swh_use_id_p = calc_vals["swh_use_id_p"]

                is_swh_use_none_b = calc_vals["is_swh_use_none_b"]
                is_swh_use_none_p = calc_vals["is_swh_use_none_p"]

                swh_use_use_units_b = calc_vals["swh_use_use_units_b"]
                swh_use_use_units_p = calc_vals["swh_use_use_units_p"]

                swh_use_multiplier_schedule_b = calc_vals[
                    "swh_use_multiplier_schedule_b"
                ]
                swh_use_multiplier_schedule_p = calc_vals[
                    "swh_use_multiplier_schedule_p"
                ]
                swh_use_temperature_at_fixture_b = calc_vals[
                    "swh_use_temperature_at_fixture_b"
                ]
                swh_use_temperature_at_fixture_p = calc_vals[
                    "swh_use_temperature_at_fixture_p"
                ]
                swh_use_water_mains_temperature_schedule_b = calc_vals[
                    "swh_use_water_mains_temperature_schedule_b"
                ]
                swh_use_water_mains_temperature_schedule_p = calc_vals[
                    "swh_use_water_mains_temperature_schedule_p"
                ]
                swh_use_served_by_distribution_system_b = calc_vals[
                    "swh_use_served_by_distribution_system_b"
                ]
                swh_use_served_by_distribution_system_p = calc_vals[
                    "swh_use_served_by_distribution_system_p"
                ]
                swh_use_design_supply_water_temperature_b = calc_vals[
                    "swh_use_design_supply_water_temperature_b"
                ]
                swh_use_design_supply_water_temperature_p = calc_vals[
                    "swh_use_design_supply_water_temperature_p"
                ]
                is_heat_recovered_by_drain_b = calc_vals["is_heat_recovered_by_drain_b"]
                is_heat_recovered_by_drain_p = calc_vals["is_heat_recovered_by_drain_p"]
                is_recovered_heat_used_by_cold_side_feed_b = calc_vals[
                    "is_recovered_heat_used_by_cold_side_feed_b"
                ]
                is_recovered_heat_used_by_cold_side_feed_p = calc_vals[
                    "is_recovered_heat_used_by_cold_side_feed_p"
                ]

                rule_note = ""
                if not is_swh_use_none_b and is_swh_use_none_p:
                    rule_note = f"{swh_use_id_p} exists in the proposed model, but not in the baseline."
                elif is_swh_use_none_b and not is_swh_use_none_p:
                    rule_note = f"{rule_note} {swh_use_id_b} exists in the baseline, but not in the proposed model."
                else:
                    if swh_use_use_units_b != swh_use_use_units_p:
                        rule_note = f"{rule_note} {swh_use_id_b} Service water heating use units are inconsistent between proposed and baseline models."

                    if swh_use_multiplier_schedule_b != swh_use_multiplier_schedule_p:
                        rule_note = f"{rule_note} {swh_use_id_b} Service Water Heating Use schedules do not match."
                    if (
                        swh_use_temperature_at_fixture_b
                        != swh_use_temperature_at_fixture_p
                    ):
                        rule_note = f"{rule_note} {swh_use_id_b} the temperature at fixture is not the same between Proposed and Baseline."
                    if (
                        swh_use_water_mains_temperature_schedule_b
                        != swh_use_water_mains_temperature_schedule_p
                    ):
                        rule_note = f"{rule_note} {swh_use_id_b} Service Water Heating Distribution System entering main water temperature schedules do not match."
                    if is_heat_recovered_by_drain_b != is_heat_recovered_by_drain_p:
                        rule_note = f"{rule_note} {swh_use_id_b} Heat recovered by drain do not match."
                    if (
                        is_recovered_heat_used_by_cold_side_feed_b
                        != is_recovered_heat_used_by_cold_side_feed_p
                    ):
                        rule_note = f"{rule_note} {swh_use_id_b} Recovered heat used by cold side feed do not match."
                    if (
                        swh_use_served_by_distribution_system_b
                        != swh_use_served_by_distribution_system_p
                    ):
                        rule_note = f"{rule_note} {swh_use_id_b} Service water heating distribution system that serves this water heating use units are inconsistent between proposed and baseline models."
                    if (
                        swh_use_design_supply_water_temperature_b
                        != swh_use_design_supply_water_temperature_p
                    ):
                        rule_note = f"{rule_note} {swh_use_id_b} Service Water Heating Distribution System design water supply temperatures do not match."
                    if swh_use_b < swh_use_p:
                        rule_note = f"{rule_note} {swh_use_id_b} Proposed Service Water Heating Use is greater than the baseline."

                return rule_note
