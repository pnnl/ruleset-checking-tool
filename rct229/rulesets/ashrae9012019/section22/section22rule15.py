from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.schema.config import ureg
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

TEMP_LOW_LIMIT_55F = 55 * ureg("degF")
TEMP_HIGH_LIMIT_90F = 90 * ureg("degF")


class PRM9012019Rule79g01(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule79g01, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule79g01.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-15",
            description="The baseline heat rejection device shall have the approach calculated according to the equation 25.72 - (0.24*WB), valid for evaporation design wet-bulb temperatures from 55°F to 90°F.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return {"heat_rejection_loop_ids_b": heat_rejection_loop_ids_b}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule79g01.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["approach", "loop", "design_wetbulb_temperature"],
                },
                precision={
                    "approach_b": {
                        "precision": 0.01,
                        "unit": "K",
                    },
                    "design_wetbulb_temp_b_low_limit": {
                        "precision": 0.01,
                        "unit": "K",
                    },
                    "design_wetbulb_temp_b_high_limit": {
                        "precision": 0.01,
                        "unit": "K",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]
            heat_rejection_loop_b = heat_rejection_b["loop"]
            design_wetbulb_temp_b = heat_rejection_b["design_wetbulb_temperature"]

            return (
                heat_rejection_loop_b in heat_rejection_loop_ids_b
                and (
                    design_wetbulb_temp_b > TEMP_LOW_LIMIT_55F
                    or self.precision_comparison["design_wetbulb_temp_b_low_limit"](
                        design_wetbulb_temp_b, TEMP_LOW_LIMIT_55F
                    )
                )
                and (
                    design_wetbulb_temp_b < TEMP_HIGH_LIMIT_90F
                    or self.precision_comparison["design_wetbulb_temp_b_high_limit"](
                        design_wetbulb_temp_b, TEMP_HIGH_LIMIT_90F
                    )
                )
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            approach_b = heat_rejection_b["approach"]
            target_approach_b = 25.72 * ureg("degF") - (
                0.24 * heat_rejection_b["design_wetbulb_temperature"].to(ureg.F)
            )

            return {
                "approach_b": CalcQ("temperature_difference", approach_b),
                "target_approach_b": CalcQ("temperature_difference", target_approach_b),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            approach_b = calc_vals["approach_b"]
            target_approach_b = calc_vals["target_approach_b"]

            return self.precision_comparison["approach_b"](
                target_approach_b.to(ureg.kelvin), approach_b
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            approach_b = calc_vals["approach_b"]
            target_approach_b = calc_vals["target_approach_b"]

            return std_equal(target_approach_b.to(ureg.kelvin), approach_b)
