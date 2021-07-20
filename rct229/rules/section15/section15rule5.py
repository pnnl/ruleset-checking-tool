from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_8_4_4_eff import table_8_4_4_eff, table_8_4_4_in_range
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals

_DRY_TYPE = schema_enums["TransformerType"].DRY_TYPE.name


class Section15Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule5, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, True, False),
            each_rule=Section15Rule5.TransformerRule(),
            index_rmr="user",
            id="15-5",
            description="Transformer efficiency reported in Baseline RMR equals Table 8.4.4",
            rmr_context="transformers",
            match_by="name",
        )

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule5.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, True, False),
                required_fields={
                    "$": ["capacity", "efficiency", "type", "phase"],
                },
            )

        def is_applicable(self, context, data=None):
            # Provide conversion from VA to kVA
            user_transformer_kVA = context.user["capacity"] / 1000
            baseline_transformer_kVA = context.baseline["capacity"] / 1000
            user_transformer_type = context.user["type"]
            user_transformer_phase = context.user["phase"]
            user_transformer_efficiency = context.user["efficiency"]
            user_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=user_transformer_phase, kVA=user_transformer_kVA
            )

            baseline_transformer_type = context.baseline["type"]
            baseline_transformer_phase = context.baseline["phase"]
            baseline_transformer_capacity_in_range = table_8_4_4_in_range(
                phase=baseline_transformer_phase, kVA=baseline_transformer_kVA
            )

            return (
                user_transformer_type == _DRY_TYPE
                and user_transformer_capacity_in_range
                and user_transformer_efficiency
                >= table_8_4_4_eff(
                    phase=user_transformer_phase, kVA=user_transformer_kVA
                )
                and baseline_transformer_type == _DRY_TYPE
                and baseline_transformer_capacity_in_range
            )

        def get_calc_vals(self, context, data=None):
            baseline_transformer_phase = context.baseline["phase"]
            # Convert from VA to user_kVA
            baseline_transformer_kVA = context.baseline["capacity"] / 1000

            return {
                "baseline_transformer_efficiency": context.baseline["efficiency"],
                "required_baseline_transformer_efficiency": table_8_4_4_eff(
                    phase=baseline_transformer_phase, kVA=baseline_transformer_kVA
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):

            # TODO: Allow tolerance?
            return (
                calc_vals["baseline_transformer_efficiency"]
                == calc_vals["required_baseline_transformer_efficiency"]
            )
