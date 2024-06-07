from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_schedule


class Section16Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(Section16Rule2, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False,
                BASELINE_0=True,
                PROPOSED=True,
            ),
            each_rule=Section16Rule2.RuleSetModelDescriptionRule(),
            index_rmd=BASELINE_0,
            id="16-2",
            description="The baseline elevator motor use shall be modeled with the same schedule as the proposed design. Rule Assertion: B-RMD = P-RMD",
            ruleset_section_title="Elevators",
            standard_section="Section G3.1",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={"$": ["calendar"], "$.calendar": ["is_leap_year"]},
            data_items={"is_leap_year_b": (BASELINE_0, "calendar/is_leap_year")},
        )

    class RuleSetModelDescriptionRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section16Rule2.RuleSetModelDescriptionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section16Rule2.RuleSetModelDescriptionRule.ElevatorRule(),
                index_rmd=BASELINE_0,
                list_path="buildings[*].elevators[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            elevators_list_b = find_all("$.buildings[*].elevators[*]", rmd_b)
            elevators_list_p = find_all("$.buildings[*].elevators[*]", rmd_p)

            return elevators_list_p and elevators_list_b

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            motor_use_schedule_b = {
                sch_id: find_exactly_one_schedule(rmd_b, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].elevators[*].cab_motor_multiplier_schedule", rmd_b
                )
            }
            motor_use_schedule_p = {
                sch_id: find_exactly_one_schedule(rmd_p, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].elevators[*].cab_motor_multiplier_schedule", rmd_p
                )
            }
            return {
                "motor_use_schedule_b": motor_use_schedule_b,
                "motor_use_schedule_p": motor_use_schedule_p,
            }

        class ElevatorRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section16Rule2.RuleSetModelDescriptionRule.ElevatorRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=True,
                    ),
                )

            def get_calc_vals(self, context, data=None):
                elevator_b = context.BASELINE_0
                elevator_p = context.PROPOSED

                motor_use_schedule_b = getattr_(
                    elevator_b, "elevators", "cab_motor_multiplier_schedule"
                )
                motor_use_schedule_p = getattr_(
                    elevator_p, "elevators", "cab_motor_multiplier_schedule"
                )

                is_leap_year_b = data["is_leap_year_b"]
                motor_use_schedule_b = data["motor_use_schedule_b"][
                    motor_use_schedule_b
                ]
                motor_use_schedule_p = data["motor_use_schedule_p"][
                    motor_use_schedule_p
                ]

                mask_schedule = (
                    [1] * LeapYear.LEAP_YEAR_HOURS
                    if is_leap_year_b
                    else [1] * LeapYear.REGULAR_YEAR_HOURS
                )

                sch_total_hours_matched = compare_schedules(
                    motor_use_schedule_b,
                    motor_use_schedule_p,
                    mask_schedule,
                    is_leap_year_b,
                )["total_hours_matched"]

                return {
                    "motor_use_schedule_len_b": len(motor_use_schedule_b),
                    "motor_use_schedule_len_p": len(motor_use_schedule_p),
                    "sch_total_hours_matched": sch_total_hours_matched,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                sch_total_hours_matched = calc_vals["sch_total_hours_matched"]
                motor_use_schedule_len_b = calc_vals["motor_use_schedule_len_b"]
                motor_use_schedule_len_p = calc_vals["motor_use_schedule_len_p"]

                return (
                    sch_total_hours_matched
                    == motor_use_schedule_len_b
                    == motor_use_schedule_len_p
                )
