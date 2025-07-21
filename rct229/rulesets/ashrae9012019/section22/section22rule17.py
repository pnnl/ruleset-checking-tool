from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

FAN_SHAFT_POWER_FACTOR = 0.9
HEAT_REJ_EFF_LIMIT = 38.2 * ureg("gpm/hp")


class PRM9012019Rule04g06(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule04g06, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule04g06.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-17",
            description="The baseline heat rejection device shall have an efficiency of 38.2 gpm/hp.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0

        return bool(find_all("$.heat_rejections[*]", rmd_b))

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return {"heat_rejection_loop_ids_b": heat_rejection_loop_ids_b}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule04g06.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["loop"],
                },
                precision={
                    "heat_rejection_efficiency_b": {
                        "precision": 0.1,
                        "unit": "gpm/hp",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]
            heat_rejection_loop_b = heat_rejection_b["loop"]

            return heat_rejection_loop_b in heat_rejection_loop_ids_b

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0

            fully_calculated = False
            heat_rejection_fan_b = heat_rejection_b.get("fan")
            heat_rejection_efficiency_b = None
            fan_shaft_power_defined_b = False
            if heat_rejection_fan_b is not None:
                if heat_rejection_fan_b.get("motor_nameplate_power"):
                    rated_water_flowrate_b = heat_rejection_b.get(
                        "rated_water_flowrate", ZERO.FLOW
                    ).to("gpm")

                    fan_motor_nameplate_power_b = heat_rejection_fan_b[
                        "motor_nameplate_power"
                    ].to("hp")

                    heat_rejection_efficiency_b = (
                        0.0
                        if fan_motor_nameplate_power_b == ZERO.POWER
                        else rated_water_flowrate_b / fan_motor_nameplate_power_b
                    )
                    fully_calculated = True

                elif heat_rejection_fan_b.get("shaft_power"):
                    fan_shaft_power_defined_b = True

                    motor_nameplate_hp_b = (
                        heat_rejection_fan_b["shaft_power"].to("hp")
                        / FAN_SHAFT_POWER_FACTOR
                    )

                    heat_rejection_efficiency_b = (
                        0.0
                        if motor_nameplate_hp_b == ZERO.POWER
                        else heat_rejection_b.get("rated_water_flowrate", ZERO.FLOW).to(
                            "gpm"
                        )
                        / motor_nameplate_hp_b
                    )

            return {
                "heat_rejection_efficiency_b": CalcQ(
                    "liquid_flow_rate_per_power", heat_rejection_efficiency_b
                ),
                "fan_shaft_power_defined_b": fan_shaft_power_defined_b,
                "fully_calculated": fully_calculated,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            heat_rejection_efficiency_b = calc_vals["heat_rejection_efficiency_b"]
            fully_calculated = calc_vals["fully_calculated"]

            return not fully_calculated or heat_rejection_efficiency_b is None

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            heat_rejection_efficiency_b = calc_vals["heat_rejection_efficiency_b"]
            fully_calculated = calc_vals["fully_calculated"]

            undetermined_msg = ""
            if heat_rejection_efficiency_b is None:
                # Case 5
                undetermined_msg = "The heat rejection fan motor nameplate power was not given, nor was the fan shaft power. We were unable to calculate the efficiency."
            elif not fully_calculated:
                if self.precision_comparison["heat_rejection_efficiency_b"](
                    heat_rejection_efficiency_b, HEAT_REJ_EFF_LIMIT
                ):
                    # Case 3
                    undetermined_msg = (
                        "The heat rejection fan motor nameplate power was not given, so we calculated the fan motor nameplate power based on the equation: Motor Nameplate Power = Fan Shaft Power / LF, where LF = 90%. "
                        "Based on this calculation for motor nameplate power, we calculated a correct efficiency of 38.2 gpm/hp."
                    )
                else:
                    # Case 4
                    undetermined_msg = (
                        f"The heat rejection fan motor nameplate power was not given, so we calculated the fan motor nameplate power based on the equation: Motor Nameplate Power = Fan Shaft Power / LF, where LF = 90%. "
                        f"Based on this calculation for motor nameplate power, we calculated an efficiency of {heat_rejection_efficiency_b} gpm/hp."
                    )

            return undetermined_msg

        def rule_check(self, context, calc_vals=None, data=None):
            heat_rejection_efficiency_b = calc_vals["heat_rejection_efficiency_b"]

            return self.precision_comparison["heat_rejection_efficiency_b"](
                heat_rejection_efficiency_b, HEAT_REJ_EFF_LIMIT
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            heat_rejection_efficiency_b = calc_vals["heat_rejection_efficiency_b"]

            return std_equal(heat_rejection_efficiency_b, HEAT_REJ_EFF_LIMIT)
