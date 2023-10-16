from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all


class Section12Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(Section12Rule1, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, True, False),
            each_rule=Section12Rule1.BuildingRule(),
            index_rmr="user",
            id="12-1",
            description=(
                "Number of spaces modeled in User RMR and Baseline RMR are the same"
            ),
            ruleset_section_title="Receptacle",
            standard_section="Section Table G3.1-12 Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section12Rule1.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, True, False),
            )

        def get_calc_vals(self, context, data=None):
            user_spaces = find_all("$..spaces[*]", context.USER)
            baseline_spaces = find_all("$..spaces[*]", context.BASELINE_0)
            return {
                "num_user_spaces": len(user_spaces),
                "num_baseline_spaces": len(baseline_spaces),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return calc_vals["num_user_spaces"] == calc_vals["num_baseline_spaces"]
