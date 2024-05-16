from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_1_fins import table_G3_9_1_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_2_fins import table_G3_9_2_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_3_fins import table_G3_9_3_lookup
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
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
                PROPOSED=True,
            ),
            each_rule=Section16Rule1.ElevatorRule(),
            index_rmd=BASELINE_0,
            id="16-1",
            description="The elevator peak motor power shall be calculated according to the equation in Table G3.1-16.",
            ruleset_section_title="Elevators",
            standard_section="Section G3.1",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].elevators[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_p = context.PROPOSED

        return find_all("$.buildings[*].elevators", rmd_p)

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

            total_floors_served_b = getattr_(
                elevator_b, "elevator", "number_of_floors_served"
            )
            elevator_motor_power_b = getattr_(elevator_b, "elevator", "motor_power")
            elevator_cab_weight_b = getattr_(elevator_b, "elevator", "cab_weight")
            elevator_cab_counterweight_b = getattr_(
                elevator_b, "elevator", "cab_counterweight"
            )
            elevator_design_load_b = getattr_(elevator_b, "elevator", "design_load")
            elevator_speed_b = getattr_(elevator_b, "elevator", "speed")

            elevator_mechanical_efficiency_b = table_G3_9_2_lookup(
                total_floors_served_b
            )["mechanical_efficiency"]

            # From Table G3.1 16 Elevators
            # bhp = (Weight of Car + Rated Load – Counterweight) × Speed of Car / (33, 000 × h_mechanical)
            # P_m = bhp x 746 / h_motor
            # Where,
            #       Weight of Car:  the proposed design elevator car weight, lb
            #       Rated Load: the proposed design elevator load at which to operate, lb
            #       Counterweight of Car: the elevator car counterweight, from Table G3.9.2, lb
            #       Speed of Car: the speed of the proposed elevator, ft/min
            #       h_mechanical: the mechanical efficiency of the elevator from Table G3.9.2
            #       h_motor: the motor efficiency from Table G3.9.2
            #       Pm: peak elevator motor power, W
            motor_brake_horsepower_b = (
                (
                    elevator_cab_weight_b * ureg("lb")
                    + elevator_design_load_b * ureg("lb")
                    - elevator_cab_counterweight_b * ureg("lb")
                )
                * elevator_speed_b
                * ureg("ft/min")
                / (33000 * elevator_mechanical_efficiency_b)
            )
            elevator_motor_efficiency_b = (
                table_G3_9_1_lookup(motor_brake_horsepower_b)["motor_efficiency"]
                if total_floors_served_b > 4
                else table_G3_9_3_lookup(motor_brake_horsepower_b)["motor_efficiency"]
            )
            expected_peak_motor_power_b = (
                motor_brake_horsepower_b.m
                * ureg("hp")
                * 746
                / elevator_motor_efficiency_b
            )

            return {
                "expected_peak_motor_power_b": CalcQ(
                    "electric_power", expected_peak_motor_power_b
                ),
                "elevator_motor_power_b": CalcQ(
                    "electric_power", elevator_motor_power_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            expected_peak_motor_power_b = calc_vals["expected_peak_motor_power_b"]
            elevator_motor_power_b = calc_vals["elevator_motor_power_b"]

            return std_equal(expected_peak_motor_power_b, elevator_motor_power_b)
