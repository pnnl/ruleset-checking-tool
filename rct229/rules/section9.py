from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rule_engine.utils import _assert_equal_rule, _select_equal_or_lesser
from rct229.utils.jsonpath_utils import find_all

# Rule Definitions for Section 9 of 90.1-2019 Appendix G


# ------------------------


class Section9Rule6_jb(RuleDefinitionListIndexedBase):
    """Rule 6-jb of ASHRAE 90.1-2019 Appendix G Section 9 (Lighting)"""

    def __init__(self):
        super(Section15Rule3, self).__init__(
            id="9-6-jb",
            description="For the proposed building, each space has the same lighting power as the corresponding space in the U-RMR",
            rmr_context="buildings",
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section9Rule6_jb.BuildingRule(),
            index_rmr="proposed",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section9Rule6_jb.BuildingRule, self).__init__(
                list_path="$..space[*]",
                rmrs_used=UserBaselineProposedVals(True, False, True),
                each_rule=Section9Rule6_jb.BuildingRule.SpaceRule(),
                index_rmr="proposed",
            )

            class SpaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section9Rule6_jb.BuildingRule.BuildingSegmentRule.ThermalBlockRule.ZoneRule.SpaceRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(True, False, True),
                    )

                def get_calc_vals(self, context, data=None):
                    return {
                        "user_space_lighting_power": 10,
                        "proposed_space_lighting_power": 10,
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    return (
                        calc_vals["user_space_lighting_power"]
                        == calc_vals["proposed_space_lighting_power"]
                    )


# ------------------------
