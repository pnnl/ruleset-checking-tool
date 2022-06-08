from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all


class Section15Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule4, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, True, False),
            each_rule=Section15Rule4.TransformerRule(),
            index_rmr="user",
            id="15-4",
            description="User RMR transformer id in Baseline RMR",
            rmr_context="ruleset_model_instances/0/transformers",
        )

    def create_data(self, context, data):
        # Get the Baseline transformer ids
        return find_all("[*].id", context.baseline)

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule4.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, False),
            )

        def get_calc_vals(self, context, data=None):
            return {
                "user_transformer_id": context.user["id"],
                "baseline_transformer_ids": data,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return (
                calc_vals["user_transformer_id"]
                in calc_vals["baseline_transformer_ids"]
            )
