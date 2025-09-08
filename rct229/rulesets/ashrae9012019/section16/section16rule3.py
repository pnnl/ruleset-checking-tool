from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_schedule


class PRM9012019Rule92n36(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(PRM9012019Rule92n36, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False,
                BASELINE_0=False,
                PROPOSED=True,
            ),
            each_rule=PRM9012019Rule92n36.RuleSetModelDescriptionRule(),
            index_rmd=PROPOSED,
            id="16-3",
            description="The elevator cab ventilation fan shall be modeled with the same schedule as the elevator motor.",
            ruleset_section_title="Elevators",
            standard_section="Section G3.1",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RuleSetModelDescriptionRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule92n36.RuleSetModelDescriptionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=PRM9012019Rule92n36.RuleSetModelDescriptionRule.ElevatorRule(),
                index_rmd=PROPOSED,
                list_path="buildings[*].elevators[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_p = context.PROPOSED

            return find_all("$.buildings[*].elevators[*]", rmd_p)

        def create_data(self, context, data):
            rmd_p = context.PROPOSED

            cab_ventilation_schedule_p = {
                sch_id: find_exactly_one_schedule(rmd_p, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].elevators[*].cab_ventilation_fan_multiplier_schedule",
                    rmd_p,
                )
            }
            motor_use_schedule_p = {
                sch_id: find_exactly_one_schedule(rmd_p, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].elevators[*].cab_motor_multiplier_schedule",
                    rmd_p,
                )
            }

            return {
                "cab_ventilation_schedule_p": cab_ventilation_schedule_p,
                "motor_use_schedule_p": motor_use_schedule_p,
            }

        class ElevatorRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule92n36.RuleSetModelDescriptionRule.ElevatorRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=False,
                        PROPOSED=True,
                    ),
                )

            def get_calc_vals(self, context, data=None):
                elevator_p = context.PROPOSED

                cab_ventilation_fan_multiplier_schedule_p = getattr_(
                    elevator_p, "elevators", "cab_ventilation_fan_multiplier_schedule"
                )
                cab_ventilation_schedule_p = data["cab_ventilation_schedule_p"][
                    cab_ventilation_fan_multiplier_schedule_p
                ]

                cab_motor_multiplier_schedule_p = getattr_(
                    elevator_p, "elevators", "cab_motor_multiplier_schedule"
                )
                motor_use_schedule_p = data["motor_use_schedule_p"][
                    cab_motor_multiplier_schedule_p
                ]

                mask_schedule = [1] * len(cab_ventilation_schedule_p)

                sch_total_hours_matched = compare_schedules(
                    cab_ventilation_schedule_p,
                    motor_use_schedule_p,
                    mask_schedule,
                )["total_hours_matched"]

                return {
                    "sch_total_hours_matched": sch_total_hours_matched,
                    "cab_ventilation_schedule_len_p": len(cab_ventilation_schedule_p),
                    "motor_use_schedule_len_p": len(motor_use_schedule_p),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                sch_total_hours_matched = calc_vals["sch_total_hours_matched"]
                cab_ventilation_schedule_len_p = calc_vals[
                    "cab_ventilation_schedule_len_p"
                ]
                motor_use_schedule_len_p = calc_vals["motor_use_schedule_len_p"]

                return (
                    sch_total_hours_matched
                    == cab_ventilation_schedule_len_p
                    == motor_use_schedule_len_p
                )
