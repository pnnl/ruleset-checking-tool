from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import (RuleDefinitionBase,
                                          RuleDefinitionListIndexedBase)
from rct229.rule_engine.user_baseline_proposed_vals import \
    UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all

# Rule Definitions for Section 12 of 90.1-2019 Appendix G

# ------------------------


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
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section12Rule1.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, True, False),
            )

        def get_calc_vals(self, context, data=None):
            user_spaces = find_all("$..spaces[*]", context.user)
            baseline_spaces = find_all("$..spaces[*]", context.baseline)
            return {
                "num_user_spaces": len(user_spaces),
                "num_baseline_spaces": len(baseline_spaces),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return calc_vals["num_user_spaces"] == calc_vals["num_baseline_spaces"]


# ------------------------


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


# ------------------------


class Section12Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(Section12Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section12Rule3.BuildingRule(),
            index_rmr="user",
            id="12-3",
            description=("User RMR Space ID in Proposed RMR"),
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section12Rule3.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                each_rule=Section12Rule3.BuildingRule.SpaceRule(),
                index_rmr="user",
                list_path="$..spaces[*]",  # All spaces in the buliding
            )

        def create_data(self, context, data):
            # Get the Proposed space id values
            return {"proposed_space_ids": find_all("$..spaces[*].id", context.proposed)}

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section12Rule3.BuildingRule.SpaceRule, self).__init__(
                    # No longer need the proposed RMR
                    rmrs_used=UserBaselineProposedVals(True, False, False)
                )

            def get_calc_vals(self, context, data=None):
                return {
                    "user_space_id": context.user["id"],
                }

            def rule_check(self, context, calc_vals, data):
                return calc_vals["user_space_id"] in data["proposed_space_ids"]


# ------------------------
