from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals


class Section15Rule2(RuleDefinitionBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        rmrs_used = UserBaselineProposedVals(True, False, True)
        id = "15-2"
        description = (
            "Number of transformers modeled in User RMR and Proposed RMR are the same"
        )
        rmr_context = "transformers"
        super(Section15Rule2, self).__init__(rmrs_used, id, description, rmr_context)

    def is_applicable(self, context, data=None):
        return len(context.user) > 0

    def get_calc_vals(self, context, data=None):
        return {
            "num_user_transformers": len(context.user),
            "num_proposed_transformers": len(context.proposed),
        }

    def rule_check(self, context, calc_vals=None, data=None):
        return (
            calc_vals["num_user_transformers"] == calc_vals["num_proposed_transformers"]
        )

