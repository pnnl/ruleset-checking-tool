from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one_with_field_value


class Section5Rule45(RuleDefinitionListIndexedBase):
    """Rule 45 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule45, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section5Rule45.RuleSetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="5-45",
            description="The infiltration schedules are the same in the proposed RMD as in the baseline RMD.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={"$": ["calendar"], "$.calendar": ["is_leap_year"]},
            data_items={"is_leap_year": (BASELINE_0, "calendar/is_leap_year")},
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule45.RuleSetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section5Rule45.RuleSetModelInstanceRule.ZoneRule(),
                index_rmd=BASELINE_0,
                list_path="buildings[*].building_segments[*].zones[*]",
                required_fields={"$": ["schedules"]},
            )

        def create_data(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            return {
                "schedules_b": rmd_b["schedules"],
                "schedules_p": rmd_p["schedules"],
            }

        # TODO we may need to add a building level for reporting purpose in the future.

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule45.RuleSetModelInstanceRule.ZoneRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["infiltration"],
                        "$.infiltration": ["multiplier_schedule"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                schedules_b = data["schedules_b"]
                schedules_p = data["schedules_p"]

                mask_schedule = [1] * (
                    LeapYear.LEAP_YEAR_HOURS
                    if data["is_leap_year"]
                    else LeapYear.REGULAR_YEAR_HOURS
                )

                infiltration_b = zone_b["infiltration"]
                infiltration_p = zone_p["infiltration"]

                return compare_schedules(
                    # search for the schedule used in infiltration data group.
                    # Set to empty list if non-matched,
                    # raise exception if not hourly schedule or the hourly_values key is missing
                    getattr_(
                        find_one_with_field_value(
                            "$[*]",
                            "id",
                            infiltration_b["multiplier_schedule"],
                            schedules_b,
                        ),
                        "schedules",
                        "hourly_values",
                    ),
                    getattr_(
                        find_one_with_field_value(
                            "$[*]",
                            "id",
                            infiltration_p["multiplier_schedule"],
                            schedules_p,
                        ),
                        "schedules",
                        "hourly_values",
                    ),
                    mask_schedule,
                    is_leap_year=data["is_leap_year"],
                )

            def rule_check(self, context, calc_vals=None, data=None):
                total_hours_compared = calc_vals["total_hours_compared"]
                total_hours_matched = calc_vals["total_hours_matched"]
                # total_hours_compared needs to be greater than 0.0
                return (
                    total_hours_compared > 0.0
                    and total_hours_compared == total_hours_matched
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                elfh_difference = calc_vals["eflh_difference"]
                return (
                    f"Baseline and proposed infiltration schedules are not the same. "
                    f"The difference between baseline EFLH to proposed EFLH is equal to {elfh_difference}."
                )
