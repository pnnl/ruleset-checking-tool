from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_rmi_dict,
)
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_exactly_one

CONDITIONED_ZONE_TYPE = [
    ZCC.CONDITIONED_MIXED,
    ZCC.CONDITIONED_NON_RESIDENTIAL,
    ZCC.CONDITIONED_RESIDENTIAL,
]
MANUAL_CHECK_MSG = "There is a humidity schedule mismatch between the baseline and proposed rmrs. Fail unless Table G3.1 #4 baseline column exception #s 1 and/or 2 are applicable"
FAIL_MSG_B = (
    "Fail because a humidity schedule is defined in the B_RMR but not in the P_RMR."
)
FAIL_MSG_P = "Fail because a humidity schedule is undefined in the B_RMR but is defined in the P_RMR."


class Section4Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 4 (Airside System)"""

    def __init__(self):
        super(Section4Rule2, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$": ["weather", "calendar"],
                "weather": ["climate_zone"],
                "calendar": ["is_leap_year"],
            },
            each_rule=Section4Rule2.RuleSetModelInstanceRule(),
            index_rmr=BASELINE_0,
            id="4-2",
            description="Humidity Control Setpoints shall be the same for proposed design and baseline building design.",
            ruleset_section_title="Airside System",
            standard_section="Section G3.1-4 Schedule Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    def create_data(self, context, data=None):
        rmr_b = context.BASELINE_0
        return {
            "climate_zone": rmr_b["weather"]["climate_zone"],
            "is_leap_year_b": rmr_b["calendar"]["is_leap_year"],
        }

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section4Rule2.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section4Rule2.RuleSetModelInstanceRule.ZoneRule(),
                index_rmr=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].zones[*]",
            )

        def create_data(self, context, data=None):
            rmi_b = context.BASELINE_0
            rmi_p = context.PROPOSED
            return {
                "schedules_b": rmi_b.get("schedules"),
                "schedules_p": rmi_p.get("schedules"),
                "zcc_dict_b": get_zone_conditioning_category_rmi_dict(
                    data["climate_zone"], rmi_b
                ),
            }

        def list_filter(self, context_item, data):
            zcc_dict_b = data["zcc_dict_b"]
            zone_b = context_item.BASELINE_0
            return zcc_dict_b[zone_b["id"]] in CONDITIONED_ZONE_TYPE

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(Section4Rule2.RuleSetModelInstanceRule.ZoneRule, self,).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    manual_check_required_msg=MANUAL_CHECK_MSG,
                )

            def get_calc_vals(self, context, data=None):
                is_leap_year = data["is_leap_year_b"]
                number_of_hours = (
                    LeapYear.LEAP_YEAR_HOURS
                    if is_leap_year
                    else LeapYear.REGULAR_YEAR_HOURS
                )

                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                schedules_b = data["schedules_b"]
                schedules_p = data["schedules_p"]

                minimum_humidity_stpt_sch_id_b = zone_b.get(
                    "minimum_humidity_setpoint_schedule"
                )
                minimum_humidity_stpt_sch_id_p = zone_p.get(
                    "minimum_humidity_setpoint_schedule"
                )
                maximum_humidity_stpt_sch_id_b = zone_b.get(
                    "maximum_humidity_setpoint_schedule"
                )
                maximum_humidity_stpt_sch_id_p = zone_p.get(
                    "maximum_humidity_setpoint_schedule"
                )

                minimum_humidity_stpt_hourly_values_b = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{minimum_humidity_stpt_sch_id_b}")]',
                            schedules_b,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if schedules_b and minimum_humidity_stpt_sch_id_b
                    else [] * number_of_hours
                )

                minimum_humidity_stpt_hourly_values_p = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{minimum_humidity_stpt_sch_id_p}")]',
                            schedules_p,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if schedules_p and minimum_humidity_stpt_sch_id_p
                    else [] * number_of_hours
                )

                maximum_humidity_stpt_hourly_values_b = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{maximum_humidity_stpt_sch_id_b}")]',
                            schedules_b,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if schedules_b and maximum_humidity_stpt_sch_id_b
                    else [] * number_of_hours
                )

                maximum_humidity_stpt_hourly_values_p = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{maximum_humidity_stpt_sch_id_p}")]',
                            schedules_p,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if schedules_p and maximum_humidity_stpt_sch_id_p
                    else [] * number_of_hours
                )

                minimum_humidity_schedule_not_matched = (
                    minimum_humidity_stpt_sch_id_b
                    and minimum_humidity_stpt_sch_id_p
                    and minimum_humidity_stpt_hourly_values_b
                    != minimum_humidity_stpt_hourly_values_p
                )
                minimum_humidity_schedule_matched = (
                    minimum_humidity_stpt_sch_id_b
                    and minimum_humidity_stpt_sch_id_p
                    and minimum_humidity_stpt_hourly_values_b
                    == minimum_humidity_stpt_hourly_values_p
                ) or (
                    not minimum_humidity_stpt_sch_id_b
                    and not minimum_humidity_stpt_sch_id_p
                )

                maximum_humidity_schedule_not_matched = (
                    maximum_humidity_stpt_sch_id_b
                    and maximum_humidity_stpt_sch_id_p
                    and maximum_humidity_stpt_hourly_values_b
                    != maximum_humidity_stpt_hourly_values_p
                )
                maximum_humidity_schedule_matched = (
                    maximum_humidity_stpt_sch_id_b
                    and maximum_humidity_stpt_sch_id_p
                    and maximum_humidity_stpt_hourly_values_b
                    == maximum_humidity_stpt_hourly_values_p
                ) or (
                    not maximum_humidity_stpt_sch_id_b
                    and not maximum_humidity_stpt_sch_id_p
                )

                return {
                    "minimum_humidity_stpt_sch_id_b": minimum_humidity_stpt_sch_id_b,
                    "minimum_humidity_stpt_sch_id_p": minimum_humidity_stpt_sch_id_p,
                    "maximum_humidity_stpt_sch_id_b": maximum_humidity_stpt_sch_id_b,
                    "maximum_humidity_stpt_sch_id_p": maximum_humidity_stpt_sch_id_p,
                    "minimum_humidity_schedule_not_matched": minimum_humidity_schedule_not_matched,
                    "maximum_humidity_schedule_not_matched": maximum_humidity_schedule_not_matched,
                    "minimum_humidity_schedule_matched": minimum_humidity_schedule_matched,
                    "maximum_humidity_schedule_matched": maximum_humidity_schedule_matched,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                minimum_humidity_schedule_not_matched = calc_vals[
                    "minimum_humidity_schedule_not_matched"
                ]
                maximum_humidity_schedule_not_matched = calc_vals[
                    "maximum_humidity_schedule_not_matched"
                ]
                return (
                    minimum_humidity_schedule_not_matched
                    or maximum_humidity_schedule_not_matched
                )

            def rule_check(self, context, calc_vals=None, data=None):
                minimum_humidity_schedule_matched = calc_vals[
                    "minimum_humidity_schedule_matched"
                ]
                maximum_humidity_schedule_matched = calc_vals[
                    "maximum_humidity_schedule_matched"
                ]
                return (
                    minimum_humidity_schedule_matched
                    and maximum_humidity_schedule_matched
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                minimum_humidity_stpt_sch_id_b = calc_vals[
                    "minimum_humidity_stpt_sch_id_b"
                ]
                minimum_humidity_stpt_sch_id_p = calc_vals[
                    "minimum_humidity_stpt_sch_id_p"
                ]
                maximum_humidity_stpt_sch_id_b = calc_vals[
                    "maximum_humidity_stpt_sch_id_b"
                ]
                maximum_humidity_stpt_sch_id_p = calc_vals[
                    "maximum_humidity_stpt_sch_id_p"
                ]
                if (
                    minimum_humidity_stpt_sch_id_b
                    and not minimum_humidity_stpt_sch_id_p
                ) or (
                    maximum_humidity_stpt_sch_id_b
                    and not maximum_humidity_stpt_sch_id_p
                ):
                    return FAIL_MSG_B
                elif (
                    not minimum_humidity_stpt_sch_id_b
                    and minimum_humidity_stpt_sch_id_p
                ) or (
                    not maximum_humidity_stpt_sch_id_b
                    and maximum_humidity_stpt_sch_id_p
                ):
                    return FAIL_MSG_P
                else:
                    return ""
