from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED, USER
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
            rmds_used=produce_ruleset_model_instance(
                USER=False,
                BASELINE_0=True,
                PROPOSED=True,
            ),
            each_rule=Section16Rule2.ElevatorRule(),
            index_rmd="baseline",
            id="16-2",
            description="The baseline elevator motor use shall be modeled with the same schedule as the proposed design. Rule Assertion: B-RMD = P-RMD",
            ruleset_section_title="Elevators",
            standard_section="Section G3.1",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="ruleset_model_descriptions[0].buildings[*].elevators[*]",
            required_fields={"$": ["calendar"], "$.calendar": ["is_leap_year"]},
            data_items={"is_leap_year_b": (BASELINE_0, "calendar/is_leap_year")},
        )

    def is_applicable(self, context, data=None):
        rmd_p = context.PROPOSED

        return find_all("$.ruleset_model_descriptions[0].buildings[*].elevators", rmd_p)

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        motor_use_schedule_b = find_exactly_one_schedule(
            rmd_b, getattr_(rmd_b, "rmd", "elevators", "cab_motor_multiplier_schedule")
        )
        motor_use_schedule_p = find_exactly_one_schedule(
            rmd_p, getattr_(rmd_p, "rmd", "elevators", "cab_motor_multiplier_schedule")
        )

        return {
            "motor_use_schedule_b": motor_use_schedule_b,
            "motor_use_schedule_p": motor_use_schedule_p,
        }

    class ElevatorRule(RuleDefinitionBase):
        def __init__(self):
            super(Section16Rule2.ElevatorRule, self).__init__(
                rmds_used=produce_ruleset_model_instance(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=True,
                ),
            )

        def get_calc_vals(self, context, data=None):
            is_leap_year_b = data["is_leap_year_b"]
            motor_use_schedule_b = data["motor_use_schedule_b"]
            motor_use_schedule_p = data["motor_use_schedule_p"]

            mask_schedule = (
                [1] * LeapYear.LEAP_YEAR_HOURS
                if is_leap_year_b
                else [1] * LeapYear.REGULAR_YEAR_HOURS
            )

            compare_schedules = compare_schedules(
                motor_use_schedule_b,
                motor_use_schedule_p,
                mask_schedule,
                is_leap_year_b,
            )

            return {
                "motor_use_schedule_len_b": len(motor_use_schedule_b),
                "motor_use_schedule_len_p": len(motor_use_schedule_p),
                "compare_schedules": compare_schedules,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            compare_schedules = calc_vals["compare_schedules"]
            motor_use_schedule_len_b = calc_vals["motor_use_schedule_len_b"]
            motor_use_schedule_len_p = calc_vals["motor_use_schedule_len_p"]

            return (
                compare_schedules["total_hours_matched"]
                == motor_use_schedule_len_b
                == motor_use_schedule_len_p
            )
