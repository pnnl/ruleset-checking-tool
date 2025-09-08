from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import USER
from rct229.rulesets.ashrae9012019.data_fns.table_8_4_4_fns import (
    table_8_4_4_in_range,
    table_8_4_4_lookup,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.compare_standard_val import std_ge

_DRY_TYPE = SchemaEnums.schema_enums["TransformerOptions"].DRY_TYPE


class Section15Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule6, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=False
            ),
            each_rule=Section15Rule6.TransformerRule(),
            index_rmd=USER,
            id="15-6",
            description="Transformer efficiency reported in User RMD equals Table 8.4.4",
            ruleset_section_title="Transformer",
            standard_section="Transformers",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0/transformers",
        )

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule6.TransformerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=False, PROPOSED=False
                ),
                required_fields={
                    "$": ["capacity", "efficiency", "type", "phase"],
                },
            )

        def is_applicable(self, context, data=None):
            user_transformer_capacity = context.USER["capacity"]

            user_transformer_type = context.USER["type"]
            user_transformer_phase = context.USER["phase"]
            user_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=user_transformer_phase, capacity=user_transformer_capacity
            )

            return (
                user_transformer_type == _DRY_TYPE
                and user_transformer_capacity_in_range
            )

        def get_calc_vals(self, context, data=None):
            user_transformer_phase = context.USER["phase"]
            user_transformer_capacity = context.USER["capacity"]

            return {
                "user_transformer_efficiency": context.USER["efficiency"],
                "required_user_transformer_min_efficiency": table_8_4_4_lookup(
                    phase=user_transformer_phase, capacity=user_transformer_capacity
                )["efficiency"],
            }

        def rule_check(self, context, calc_vals=None, data=None):
            user_transformer_efficiency = calc_vals["user_transformer_efficiency"]
            required_user_transformer_min_efficiency = calc_vals[
                "required_user_transformer_min_efficiency"
            ]

            return (
                user_transformer_efficiency > required_user_transformer_min_efficiency
                or self.precision_comparison(
                    required_user_transformer_min_efficiency,
                    user_transformer_efficiency,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            user_transformer_efficiency = calc_vals["user_transformer_efficiency"]
            required_user_transformer_min_efficiency = calc_vals[
                "required_user_transformer_min_efficiency"
            ]

            return std_ge(
                required_user_transformer_min_efficiency, user_transformer_efficiency
            )
