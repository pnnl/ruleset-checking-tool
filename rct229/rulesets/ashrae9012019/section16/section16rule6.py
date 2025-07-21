from rct229.schema.config import ureg
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal
from rct229.utils.pint_utils import ZERO
from rct229.utils.pint_utils import CalcQ

REQ_ELEVATOR_CAB_VENTILATION_FAN_POWER = 0.33 * ureg("W/cfm")


class PRM9012019Rule34h06(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(PRM9012019Rule34h06, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule34h06.ElevatorRule(),
            index_rmd=BASELINE_0,
            id="16-6",
            description="When included in the proposed design, the baseline elevator cab ventilation fan power shall be 0.33 W/cfm.",
            ruleset_section_title="Elevators",
            standard_section="Table G3.1-16 Baseline Building Performance",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*].elevators[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        elevators_list_b = find_all(
            "$.ruleset_model_descriptions[0].buildings[*].elevators[*]", rmd_b
        )
        elevators_list_p = find_all(
            "$.ruleset_model_descriptions[0].buildings[*].elevators[*]", rmd_p
        )

        return elevators_list_p and elevators_list_b

    class ElevatorRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule34h06.ElevatorRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cab_ventilation_fan"],
                    "$.cab_ventilation_fan": [
                        "design_airflow",
                        "design_electric_power",
                    ],
                },
                precision={
                    "elevator_cab_ventilation_fan_power_b/elevator_cab_ventilation_fan_flow_b": {
                        "precision": 0.1,
                        "unit": "W/cfm",
                    }
                },
            )

        def get_calc_vals(self, context, data=None):
            elevator_b = context.BASELINE_0
            elevator_cab_ventilation_fan_power_b = elevator_b["cab_ventilation_fan"][
                "design_electric_power"
            ]
            assert_(
                elevator_cab_ventilation_fan_power_b > ZERO.POWER,
                "Elevator cab ventilation fan power should be " "greater than 0 W.",
            )

            elevator_cab_ventilation_fan_flow_b = elevator_b["cab_ventilation_fan"][
                "design_airflow"
            ]
            assert_(
                elevator_cab_ventilation_fan_flow_b > ZERO.FLOW,
                "Elevator cab ventilation fan flow rate should "
                "be greater than 0 cfm.",
            )

            return {
                "elevator_cab_ventilation_fan_power_b": CalcQ(
                    "electric_power", elevator_cab_ventilation_fan_power_b
                ),
                "elevator_cab_ventilation_fan_flow_b": CalcQ(
                    "air_flow_rate", elevator_cab_ventilation_fan_flow_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            elevator_cab_ventilation_fan_power_b = calc_vals[
                "elevator_cab_ventilation_fan_power_b"
            ]
            elevator_cab_ventilation_fan_flow_b = calc_vals[
                "elevator_cab_ventilation_fan_flow_b"
            ]
            return self.precision_comparison[
                "elevator_cab_ventilation_fan_power_b/elevator_cab_ventilation_fan_flow_b"
            ](
                elevator_cab_ventilation_fan_power_b
                / elevator_cab_ventilation_fan_flow_b,
                REQ_ELEVATOR_CAB_VENTILATION_FAN_POWER,
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            elevator_cab_ventilation_fan_power_b = calc_vals[
                "elevator_cab_ventilation_fan_power_b"
            ]
            elevator_cab_ventilation_fan_flow_b = calc_vals[
                "elevator_cab_ventilation_fan_flow_b"
            ]
            return std_equal(
                REQ_ELEVATOR_CAB_VENTILATION_FAN_POWER,
                elevator_cab_ventilation_fan_power_b
                / elevator_cab_ventilation_fan_flow_b,
            )
