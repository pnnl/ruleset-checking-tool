from rct229.schema.config import ureg
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal
from rct229.utils.pint_utils import ZERO
from rct229.utils.pint_utils import CalcQ

REQ_ELEVATOR_CAB_VENTILATION_FAN_POWER = 0.33 * ureg("W/cfm")


class Section16Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(Section16Rule6, self).__init__(
            rmds_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section16Rule6.ElevatorRule(),
            index_rmd=BASELINE_0,
            id="16-6",
            description="When included in the proposed design, the baseline elevator cab ventilation fan power shall be 0.33 W/cfm.",
            ruleset_section_title="Elevators",
            standard_section="Table G3.1-16 Baseline Building Performance",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="ruleset_model_descriptions[0].buildings[*].elevators[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_p = context.PROPOSED
        return find_all("$.ruleset_model_descriptions[0].buildings[*].elevators", rmd_p)

    class ElevatorRule(RuleDefinitionBase):
        def __init__(self):
            super(Section16Rule6.ElevatorRule, self).__init__(
                rmds_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cab_ventilation_fan_power", "cab_ventilation_fan_flow"]
                },
            )

        def get_calc_vals(self, context, data=None):
            elevator_b = context.BASELINE_0
            elevator_cab_ventilation_fan_power_b = elevator_b[
                "cab_ventilation_fan_power"
            ]
            elevator_cab_ventilation_fan_flow_b = elevator_b["cab_ventilation_fan_flow"]
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
            return elevator_cab_ventilation_fan_flow_b != ZERO.FLOW and std_equal(
                elevator_cab_ventilation_fan_power_b
                / elevator_cab_ventilation_fan_flow_b,
                REQ_ELEVATOR_CAB_VENTILATION_FAN_POWER,
            )