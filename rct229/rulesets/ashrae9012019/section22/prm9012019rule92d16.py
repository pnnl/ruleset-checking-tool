from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_

HEATREJECTIONFAN = SchemaEnums.schema_enums["HeatRejectionFanOptions"]
HEATREJECTION = SchemaEnums.schema_enums["HeatRejectionOptions"]


class PRM9012019Rule92d16(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule92d16, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule92d16.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-13",
            description="The baseline heat rejection device shall be an axial-fan open circuit cooling tower.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def create_data(self, context, data=None):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return {"heat_rejection_loop_ids_b": heat_rejection_loop_ids_b}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule92d16.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_type", "type"],
                },
            )

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_loop_b = getattr_(
                heat_rejection_b, "heat_rejections", "loop"
            )
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]

            return heat_rejection_loop_b in heat_rejection_loop_ids_b

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            fan_type_b = heat_rejection_b["fan_type"]
            heat_rejection_type_b = heat_rejection_b["type"]

            return {
                "fan_type_b": fan_type_b,
                "heat_rejection_type_b": heat_rejection_type_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            fan_type_b = calc_vals["fan_type_b"]
            heat_rejection_type_b = calc_vals["heat_rejection_type_b"]

            return (
                fan_type_b == HEATREJECTIONFAN.AXIAL
                and heat_rejection_type_b == HEATREJECTION.OPEN_CIRCUIT_COOLING_TOWER
            )
