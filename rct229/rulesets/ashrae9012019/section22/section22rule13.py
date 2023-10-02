from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.utils.assertions import getattr_

HEATREJECTIONFAN = schema_enums["HeatRejectionFanOptions"]
HEATREJECTION = schema_enums["HeatRejectionOptions"]


class Section22Rule13(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule13, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule13.HeatRejectionRule(),
            index_rmr="baseline",
            id="22-13",
            description="The baseline heat rejection loop shall be an axial-fan open circuit cooling tower.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.baseline
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return heat_rejection_loop_ids_b

    def create_data(self, context, data=None):
        rmd_b = context.baseline
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return {"heat_rejection_loop_ids_b": heat_rejection_loop_ids_b}

    def list_filter(self, context_item, data):
        heat_rejection_b = context_item.baseline
        heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]
        heat_rejection_loop_b = getattr_("$.loop", "loop", heat_rejection_b)

        return heat_rejection_loop_b in heat_rejection_loop_ids_b

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule13.HeatRejectionRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["fan_type", "type"],
                },
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.baseline
            fan_type_b = heat_rejection_b["fan_type"]
            heat_rejection_type_b = heat_rejection_b["heat_rejection_type "]

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
