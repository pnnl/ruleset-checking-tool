from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import USER
from rct229.rulesets.ashrae9012019.data_fns.table_8_4_4_fns import (
    table_8_4_4_in_range,
    table_8_4_4_lookup,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.std_comparisons import std_equal

_DRY_TYPE = SchemaEnums.schema_enums["TransformerOptions"].DRY_TYPE


class Section15Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule5, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section15Rule5.TransformerRule(),
            index_rmd=USER,
            id="15-5",
            description="Transformer efficiency reported in Baseline RMD equals Table 8.4.4",
            ruleset_section_title="Transformer",
            standard_section="Transformers",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0/transformers",
        )

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule5.TransformerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["capacity", "efficiency", "type", "phase"],
                },
            )

        def is_applicable(self, context, data=None):
            user_transformer_capacity = context.USER["capacity"]
            baseline_transformer_capacity = context.BASELINE_0["capacity"]
            user_transformer_type = context.USER["type"]
            user_transformer_phase = context.USER["phase"]
            user_transformer_efficiency = context.USER["efficiency"]
            user_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=user_transformer_phase, capacity=user_transformer_capacity
            )

            baseline_transformer_type = context.BASELINE_0["type"]
            baseline_transformer_phase = context.BASELINE_0["phase"]
            baseline_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=baseline_transformer_phase, capacity=baseline_transformer_capacity
            )

            return (
                user_transformer_type == _DRY_TYPE
                and user_transformer_capacity_in_range
                and user_transformer_efficiency
                >= table_8_4_4_lookup(
                    phase=user_transformer_phase, capacity=user_transformer_capacity
                )["efficiency"]
                and baseline_transformer_type == _DRY_TYPE
                and baseline_transformer_capacity_in_range
            )

        def get_calc_vals(self, context, data=None):
            baseline_transformer_phase = context.BASELINE_0["phase"]
            baseline_transformer_capacity = context.BASELINE_0["capacity"]

            return {
                "baseline_transformer_efficiency": context.BASELINE_0["efficiency"],
                "required_baseline_transformer_efficiency": table_8_4_4_lookup(
                    phase=baseline_transformer_phase,
                    capacity=baseline_transformer_capacity,
                )["efficiency"],
            }

        def rule_check(self, context, calc_vals=None, data=None):
            # TODO: Allow tolerance?
            return self.precision_comparison(
                calc_vals["baseline_transformer_efficiency"],
                calc_vals["required_baseline_transformer_efficiency"],
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            return std_equal(
                calc_vals["required_baseline_transformer_efficiency"],
                calc_vals["baseline_transformer_efficiency"],
            )
