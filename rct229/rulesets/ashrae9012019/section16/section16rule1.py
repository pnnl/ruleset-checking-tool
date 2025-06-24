from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_1_fins import table_G3_9_1_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_2_fins import table_G3_9_2_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_3_fins import table_G3_9_3_lookup
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal


class PRM9012019Rule98t42(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(PRM9012019Rule98t42, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False,
                BASELINE_0=True,
                PROPOSED=True,
            ),
            each_rule=PRM9012019Rule98t42.ElevatorRule(),
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
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        elevators_list_b = find_all("$.buildings[*].elevators[*]", rmd_b)
        elevators_list_p = find_all("$.buildings[*].elevators[*]", rmd_p)

        return elevators_list_p and elevators_list_b

    class ElevatorRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule98t42.ElevatorRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=False,
                ),
                precision={
                    "elevator_motor_power_b": {
                        "precision": 0.1,
                        "unit": "W",
                    }
                },
            )

        def get_calc_vals(self, context, data=None):
            elevator_b = context.BASELINE_0

            total_floors_served_b = getattr_(
                elevator_b, "elevators", "number_of_floors_served"
            )
            assert_(
                total_floors_served_b > 1,
                "The `number of floors served` value must be greater than 1.",
            )

            elevator_motor_power_b = getattr_(elevator_b, "elevators", "motor_power")

            elevator_cab_weight_b = getattr_(elevator_b, "elevators", "cab_weight")
            elevator_cab_counterweight_b = getattr_(
                elevator_b, "elevators", "cab_counterweight"
            )
            elevator_design_load_b = getattr_(elevator_b, "elevators", "design_load")
            assert_(
                elevator_cab_weight_b
                + elevator_design_load_b
                - elevator_cab_counterweight_b
                > ZERO.WEIGHT,
                "Elevator cab counter weight shall be smaller than the sum of cab weight and design load. A "
                "typical cab counter weight is the sum of cab weight and 40% of design load.",
            )

            elevator_speed_b = getattr_(elevator_b, "elevators", "speed")
            elevator_mechanical_efficiency_b = table_G3_9_2_lookup(
                total_floors_served_b
            )["mechanical_efficiency"]

            # From Table G3.1 16 Elevators
            # bhp (hp) = (Weight of Car + Rated Load – Counterweight) × Speed of Car / (33,000 × h_mechanical)
            # P_m (W) = bhp x 746 / h_motor
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
                    elevator_cab_weight_b.to("lb")
                    + elevator_design_load_b.to("lb")
                    - elevator_cab_counterweight_b.to("lb")
                )
                * elevator_speed_b.to("ft/min")
                / ureg("hp").to("ft*lbf/min")
                / elevator_mechanical_efficiency_b
            ).m * ureg("hp")

            elevator_motor_efficiency_b = (
                table_G3_9_1_lookup(motor_brake_horsepower_b)[
                    "full_load_motor_efficiency_for_modeling"
                ]
                if total_floors_served_b > 4
                else table_G3_9_3_lookup(motor_brake_horsepower_b)[
                    "full_load_motor_efficiency_for_modeling"
                ]
            )
            expected_peak_motor_power_b = (
                motor_brake_horsepower_b / elevator_motor_efficiency_b
            )  # We didn't include 746 because it's a conversion factor (e.g., 745.7 W = 1 hp)

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

            return self.precision_comparison["elevator_motor_power_b"](
                elevator_motor_power_b, expected_peak_motor_power_b
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            expected_peak_motor_power_b = calc_vals["expected_peak_motor_power_b"]
            elevator_motor_power_b = calc_vals["elevator_motor_power_b"]

            return std_equal(expected_peak_motor_power_b, elevator_motor_power_b)
