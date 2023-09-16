from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all


class Section15Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section15Rule3.TransformerRule(),
            index_rmr="user",
            id="15-3",
            description="User RMR transformer id in Proposed RMR",
            ruleset_section_title="Transformer",
            standard_section="Transformers",
            is_primary_rule=False,
            rmr_context="ruleset_model_descriptions/0/transformers",
        )

    def create_data(self, context, data):
        transformers_p = context.proposed
        return {"transformer_ids_p": find_all("$[*].id", transformers_p)}

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section15Rule3.TransformerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, False)
            )

        def get_calc_vals(self, context, data=None):
            return {
                "user_transformer_id": context.user["id"],
                "transformer_ids_p": data["transformer_ids_p"],
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return calc_vals["user_transformer_id"] in calc_vals["transformer_ids_p"]
