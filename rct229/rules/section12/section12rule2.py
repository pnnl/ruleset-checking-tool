from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all


class Section12Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(Section12Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section12Rule2.BuildingRule(),
            index_rmr="user",
            id="12-2",
            description=(
                "Number of spaces modeled in User RMR and Proposed RMR are the same"
            ),
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section12Rule2.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
            )

        def get_calc_vals(self, context, data=None):
            user_spaces = find_all("$..spaces[*]", context.user)
            proposed_spaces = find_all("$..spaces[*]", context.proposed)
            return {
                "num_user_spaces": len(user_spaces),
                "num_proposed_spaces": len(proposed_spaces),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return calc_vals["num_user_spaces"] == calc_vals["num_proposed_spaces"]
