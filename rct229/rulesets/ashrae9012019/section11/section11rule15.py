from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all, find_one


class Section11Rule15(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule15, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule15.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-15",
            description=(
                "Service water loads and use shall be the same for both the proposed design and baseline building design.Exceptions:(1) Energy Efficiency Measures approved by the Authority Having Jurisdiction are used in the proposed model (2) SWH energy consumption can be demonstrated to be reduced by reducing the required temperature of service mixed water, by increasing the temperature, or by increasing the temperature of the entering makeup water."
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, (g)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionBase):
        def __init__(self):
            super(Section11Rule15.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                # each_rule=Section11Rule15.RMDRule.BuildingRule(),
                # index_rmd=BASELINE_0,
                # list_path="$.buildings[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            swh_use_ids = []

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                service_water_heating_use_ids_b = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_b, building_segment["id"]
                    )
                )
                swh_use_ids.append(service_water_heating_use_ids_b)

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_p
            ):
                service_water_heating_use_ids_p = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_p, building_segment["id"]
                    )
                )
                swh_use_ids.extend(
                    [
                        swh_use_id
                        for swh_use_id in service_water_heating_use_ids_p
                        if swh_use_id not in swh_use_ids
                    ]
                )
            return len(swh_use_ids) > 0

        def get_calc_vals(self, context, data=None):
            rule_status = "pass"
            rule_note = ""
            manual_check_msg = ""
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            swh_use_ids = []

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                service_water_heating_use_ids_b = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_b, building_segment["id"]
                    )
                )
                swh_use_ids.append(service_water_heating_use_ids_b)

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_p
            ):
                service_water_heating_use_ids_p = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_p, building_segment["id"]
                    )
                )
                swh_use_ids.extend(
                    [
                        swh_use_id
                        for swh_use_id in service_water_heating_use_ids_p
                        if swh_use_id not in swh_use_ids
                    ]
                )
            for swh_use_id in swh_use_ids:
                swh_use_b = find_one(
                    "$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
                    rmd_b,
                )
                swh_use_p = find_one(
                    "$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
                    rmd_p,
                )
                if not swh_use_b and swh_use_p:
                    rule_status = "fail"
                    rule_note = (
                        rule_note
                        + swh_use_id
                        + " exists in the proposed model, but not in the baseline."
                    )
                elif swh_use_b and not swh_use_p:
                    rule_status = "fail"
                    rule_note = (
                        rule_note
                        + swh_use_id
                        + " exists in the baseline, but not in the proposed model."
                    )
                else:
                    if swh_use_b.get("use_units") != swh_use_p.get("use_units"):
                        rule_status = "fail"
                        rule_note = (
                            rule_note
                            + swh_use_id
                            + " Service water heating use units are inconsistent between proposed and baseline models. "
                        )
                    if swh_use_b.get("use_multiplier_schedule") != swh_use_p.get(
                        "use_multiplier_schedule"
                    ):
                        rule_status = "fail"
                        rule_note = (
                            rule_note
                            + swh_use_id
                            + " Service Water Heating Use schedules do not match. "
                        )

                    if swh_use_b.get("temperature_at_fixture") != swh_use_p.get(
                        "temperature_at_fixture"
                    ):
                        rule_status = "fail"
                        rule_note = (
                            rule_note
                            + swh_use_id
                            + " The temperature at fixture is not the same between Proposed and Baseline. "
                        )
                    if swh_use_b.get(
                        "entering_water_mains_temperature_schedule"
                    ) != swh_use_p.get("entering_water_mains_temperature_schedule"):
                        rule_status = "fail"
                        rule_note = (
                            rule_note
                            + swh_use_id
                            + " Service Water Heating Distribution System entering main water temperature schedules do not match. "
                        )
                    swh_dist_sys_b = swh_use_b.get("served_by_distribution_system")
                    swh_dist_sys_p = swh_use_p.get("served_by_distribution_system")
                    if swh_dist_sys_b != swh_dist_sys_p:
                        rule_status = "fail"
                        rule_note = (
                            rule_note
                            + swh_use_id
                            + " Service water heating distribution system that serves this water heating use units are "
                            "inconsistent between proposed and baseline models. "
                        )

                    if swh_dist_sys_b and swh_dist_sys_p:
                        if swh_dist_sys_b.get(
                            "design_supply_water_temperature"
                        ) != swh_dist_sys_p.get("design_supply_water_temperature"):
                            rule_status = "fail"
                            rule_note = (
                                rule_note
                                + swh_use_id
                                + " Service Water Heating Distribution System design water supply temperatures do not "
                                "match. "
                            )
                    if rule_status == "pass":
                        if swh_use_p.get("use", 0) < swh_use_b.get("use", 0):
                            rule_status = "undetermined"
                            manual_check_msg = (
                                manual_check_msg
                                + swh_use_id
                                + " Proposed Service Water Heating Use is less than the baseline.  Manually verify that reduction is due to an ECM that reduces service water heating use, such as low-flow fixtures. "
                            )
                        elif swh_use_p.get("use", 0) > swh_use_b.get("use", 0):
                            rule_status = "fail"
                            rule_note = (
                                rule_note
                                + swh_use_id
                                + " Proposed Service Water Heating Use is greater than the baseline. "
                            )
            return {
                "rule_status": rule_status,
                "rule_note": rule_note,
                "manual_check_msg": manual_check_msg,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            rule_status = calc_vals["rule_status"]
            return rule_status == "undetermined"

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            manual_check_msg = calc_vals["manual_check_msg"]
            return manual_check_msg

        def rule_check(self, context, calc_vals=None, data=None):
            rule_status = calc_vals["rule_status"]
            return rule_status == "pass"

        def get_fail_msg(self, context, calc_vals=None, data=None):
            rule_note = calc_vals["rule_note"]
            return rule_note
