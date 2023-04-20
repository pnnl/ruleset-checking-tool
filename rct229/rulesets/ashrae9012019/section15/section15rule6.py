from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.data_fns.table_8_4_4_fns import (
    table_8_4_4_in_range,
    table_8_4_4_lookup,
)

_DRY_TYPE = schema_enums["TransformerOptions"].DRY_TYPE


class Section15Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule6, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, False),
            each_rule=Section15Rule6.TransformerRule(),
            index_rmr="user",
            id="15-6",
            description="Transformer efficiency reported in User RMR equals Table 8.4.4",
            ruleset_section_title="Transformer",
            standard_section="Transformers",
            is_primary_rule=False,
            rmr_context="ruleset_model_instances/0/transformers",
        )

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule6.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, False),
                required_fields={
                    "$": ["capacity", "efficiency", "type", "phase"],
                },
            )

        def is_applicable(self, context, data=None):
            user_transformer_capacity = context.user["capacity"]

            user_transformer_type = context.user["type"]
            user_transformer_phase = context.user["phase"]
            user_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=user_transformer_phase, capacity=user_transformer_capacity
            )

            return (
                user_transformer_type == _DRY_TYPE
                and user_transformer_capacity_in_range
            )

        def get_calc_vals(self, context, data=None):
            user_transformer_phase = context.user["phase"]
            user_transformer_capacity = context.user["capacity"]

            return {
                "user_transformer_efficiency": context.user["efficiency"],
                "required_user_transformer_min_efficiency": table_8_4_4_lookup(
                    phase=user_transformer_phase, capacity=user_transformer_capacity
                )["efficiency"],
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return (
                calc_vals["user_transformer_efficiency"]
                >= calc_vals["required_user_transformer_min_efficiency"]
            )
