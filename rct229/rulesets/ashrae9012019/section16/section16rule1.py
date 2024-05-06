from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED, USER
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_1_fins import table_G3_9_1_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_2_fins import table_G3_9_2_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_3_fins import table_G3_9_3_lookup
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal


class Section16Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(Section16Rule1, self).__init__(
            rmds_used=produce_ruleset_model_instance(
                USER=False,
                BASELINE_0=True,
                PROPOSED=False,
            ),
            each_rule=Section16Rule1.ElevatorRule(),
            index_rmd="baseline",
            id="16-1",
            description="The elevator peak motor power shall be calculated according to the equation in Table G3.1-16.",
            ruleset_section_title="Elevators",
            standard_section="Section G3.1",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="ruleset_model_descriptions[0].buildings[*].elevators[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_p = context.PROPOSED

        return (
            len(
                find_all(
                    "$.ruleset_model_descriptions[0].buildings[*].elevators", rmd_p
                )
            )
            > 0
        )

    class ElevatorRule(RuleDefinitionBase):
        def __init__(self):
            super(Section16Rule1.ElevatorRule, self).__init__(
                rmds_used=produce_ruleset_model_instance(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=False,
                ),
            )

        def get_calc_vals(self, context, data=None):
            elevator_b = context.BASELINE_0

            total_floors_served_b = elevator_b.get("number_of_floors_served")
            elevator_motor_power_b = elevator_b.get("motor_power")
            elevator_cab_weight_b = elevator_b.get("cab_weight")
            elevator_cab_counterweight_b = elevator_b.get("cab_counterweight")
            elevator_design_load_b = elevator_b.get("design_load")
            elevator_speed_b = elevator_b.get("speed")

            has_undetermined = any(
                [
                    param is None
                    for param in (
                        total_floors_served_b,
                        elevator_motor_power_b,
                        elevator_cab_weight_b,
                        elevator_cab_counterweight_b,
                        elevator_design_load_b,
                        elevator_speed_b,
                    )
                ]
            )

            elevator_mechanical_efficiency_b = table_G3_9_2_lookup(
                total_floors_served_b
            )["mechanical_efficiency"]
            motor_brake_horsepower_b = (
                (
                    elevator_cab_weight_b
                    + elevator_design_load_b
                    - elevator_cab_counterweight_b
                )
                * elevator_speed_b
                / 33000
                / elevator_mechanical_efficiency_b
            )
            elevator_motor_efficiency_b = (
                table_G3_9_1_lookup(motor_brake_horsepower_b)["motor_efficiency"]
                if total_floors_served_b > 4
                else table_G3_9_3_lookup(motor_brake_horsepower_b)["motor_efficiency"]
            )
            expected_peak_motor_power_b = (
                motor_brake_horsepower_b * 746 / elevator_motor_efficiency_b
            )

            return {
                "expected_peak_motor_power_b": CalcQ(
                    "electric_power", expected_peak_motor_power_b
                ),
                "elevator_motor_power_b": CalcQ(
                    "electric_power", elevator_motor_power_b
                ),
                "has_undetermined": has_undetermined,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            has_undetermined = calc_vals["has_undetermined"]

            return has_undetermined

        def rule_check(self, context, calc_vals=None, data=None):
            expected_peak_motor_power_b = calc_vals["expected_peak_motor_power_b"]
            elevator_motor_power_b = calc_vals["elevator_motor_power_b"]

            return std_equal(expected_peak_motor_power_b, elevator_motor_power_b)
