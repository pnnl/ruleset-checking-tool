from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.compare_schedules import (
    LEAP_YEAR_HOURS,
    REGULAR_YEAR_HOURS,
    compare_schedules,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one_with_field_value


class Section5Rule45(RuleDefinitionListIndexedBase):
    """Rule 45 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule45, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section5Rule45.RuleSetModelInstanceRule(),
            index_rmr="baseline",
            id="5-45",
            description="The infiltration schedules are the same in the proposed RMR as in the baseline RMR.",
            list_path="ruleset_model_instances[0]",
            required_fields={"$": ["calendar"], "calendar": ["is_leap_year"]},
        )

    def create_data(self, context, data=None):
        rmd_b = context.baseline
        return {"is_leap_year": rmd_b["calendar"]["is_leap_year"]}

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule45.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section5Rule45.RuleSetModelInstanceRule.ZoneRule(),
                index_rmr="baseline",
                list_path="buildings[*].building_segments[*].zones[*]",
                required_fields={"$": ["schedules"]},
            )

        def create_data(self, context, data=None):
            rmd_b = context.baseline
            rmd_p = context.proposed
            return {
                **data,
                "schedules_b": rmd_b["schedules"],
                "schedules_p": rmd_p["schedules"],
            }

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule45.RuleSetModelInstanceRule.ZoneRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={
                        "$": ["infiltration"],
                        "infiltration": ["multiplier_schedule"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                zone_b = context.baseline
                zone_p = context.proposed

                schedules_b = data["schedules_b"]
                schedules_p = data["schedules_p"]

                mask_schedule = [1] * (
                    LEAP_YEAR_HOURS if data["is_leap_year"] else REGULAR_YEAR_HOURS
                )

                infiltration_b = zone_b["infiltration"]
                infiltration_p = zone_p["infiltration"]

                return compare_schedules(
                    # search for the schedule used in infiltration data group.
                    # Set to empty list if non-matched,
                    # raise exception if not hourly schedule or the hourly_values key is missing
                    getattr_(
                        find_one_with_field_value(
                            "$",
                            "id",
                            infiltration_b["multiplier_schedule"],
                            schedules_b,
                        ),
                        "schedule",
                        "hourly_values",
                    ),
                    getattr_(
                        find_one_with_field_value(
                            "$",
                            "id",
                            infiltration_p["multiplier_schedule"],
                            schedules_p,
                        ),
                        "schedule",
                        "hourly_values",
                    ),
                    mask_schedule,
                    comparison_factor=1.0,
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
