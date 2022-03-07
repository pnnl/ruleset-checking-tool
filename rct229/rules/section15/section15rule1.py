from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals


class Section15Rule1(RuleDefinitionBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        rmrs_used = UserBaselineProposedVals(True, True, False)
        id = "15-1"
        description = (
            "Number of transformers modeled in User RMR and Baseline RMR are the same"
        )
        rmr_context = "transformers"
        super(Section15Rule1, self).__init__(rmrs_used, id, description, rmr_context)

    def is_applicable(self, context, data=None):
        return len(context.user) > 0

    def get_calc_vals(self, context, data=None):
        return {
            "num_user_transformers": len(context.user),
            "num_baseline_transformers": len(context.baseline),
        }

    def rule_check(self, context, calc_vals=None, data=None):
        return (
            calc_vals["num_user_transformers"] == calc_vals["num_baseline_transformers"]
        )
