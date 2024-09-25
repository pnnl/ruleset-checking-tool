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


class Section16Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(Section16Rule5, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False,
                BASELINE_0=True,
                PROPOSED=True,
            ),
            each_rule=Section16Rule5.RuleSetModelDescriptionRule(),
            index_rmd=BASELINE_0,
            id="16-5",
            description="When included in the proposed design, the baseline elevator cab ventilation fan and lights shall operate continuously",
            ruleset_section_title="Elevators",
            standard_section="Section G3.1",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={"$": ["calendar"], "$.calendar": ["is_leap_year"]},
            data_items={"is_leap_year_b": (BASELINE_0, "calendar/is_leap_year")},
        )

    class RuleSetModelDescriptionRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section16Rule5.RuleSetModelDescriptionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section16Rule5.RuleSetModelDescriptionRule.ElevatorRule(),
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

            cab_ventilation_fan_multiplier_schedule_b = {
                sch_id: find_exactly_one_schedule(rmd_b, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].elevators[*].cab_ventilation_fan_multiplier_schedule",
                    rmd_b,
                )
            }
            cab_lighting_multiplier_schedule_b = {
                sch_id: find_exactly_one_schedule(rmd_b, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].elevators[*].cab_lighting_multiplier_schedule", rmd_b
                )
            }

            return {
                "cab_ventilation_fan_multiplier_schedule_b": cab_ventilation_fan_multiplier_schedule_b,
                "cab_lighting_multiplier_schedule_b": cab_lighting_multiplier_schedule_b,
            }

        class ElevatorRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section16Rule5.RuleSetModelDescriptionRule.ElevatorRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=False,
                    ),
                )

            def get_calc_vals(self, context, data=None):
                elevator_b = context.BASELINE_0
                is_leap_year_b = data["is_leap_year_b"]

                cab_vent_fan_multi_sch_b = getattr_(
                    elevator_b, "elevators", "cab_ventilation_fan_multiplier_schedule"
                )
                cab_vent_sch_b = data["cab_ventilation_fan_multiplier_schedule_b"][
                    cab_vent_fan_multi_sch_b
                ]

                cab_lgt_multi_sch_b = getattr_(
                    elevator_b, "elevators", "cab_lighting_multiplier_schedule"
                )
                cab_lgt_sch_b = data["cab_lighting_multiplier_schedule_b"][
                    cab_lgt_multi_sch_b
                ]

                total_hours = (
                    LeapYear.LEAP_YEAR_HOURS
                    if is_leap_year_b
                    else LeapYear.REGULAR_YEAR_HOURS
                )

                continuous_schedule = [1] * total_hours

                vent_sched_compare_data = compare_schedules(
                    cab_vent_sch_b,
                    continuous_schedule,
                    continuous_schedule,
                    is_leap_year_b,
                )["total_hours_matched"]

                light_sched_compare_data = compare_schedules(
                    cab_lgt_sch_b,
                    continuous_schedule,
                    continuous_schedule,
                    is_leap_year_b,
                )["total_hours_matched"]

                return {
                    "vent_sched_compare_data": vent_sched_compare_data,
                    "light_sched_compare_data": light_sched_compare_data,
                    "total_hours": total_hours,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                vent_sched_compare_data = calc_vals["vent_sched_compare_data"]
                light_sched_compare_data = calc_vals["light_sched_compare_data"]
                total_hours = calc_vals["total_hours"]

                return (
                    vent_sched_compare_data == light_sched_compare_data == total_hours
                )
