from numpy import sum

from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all

# Rule Definitions for Section 5 of 90.1-2019 Appendix G


# ------------------------


class Section5Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section5Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section5Rule2.BuildingRule(),
            index_rmr="proposed",
            id="5-2",
            description="Orientation is the same in user model and proposed model",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule2.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                each_rule=Section5Rule2.BuildingRule.SurfaceRule(),
                index_rmr="proposed",
                list_path="$..surfaces[*]",  # All surfaces inside the building
            )

        class SurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule2.BuildingRule.SurfaceRule, self,).__init__(
                    required_fields={
                        "$": ["azimuth"],
                    },
                    rmrs_used=UserBaselineProposedVals(True, False, True),
                )

            def get_calc_vals(self, context, data=None):
                azimuth_user = context.user["azimuth"]
                azimuth_proposed = context.proposed["azimuth"]

                return {
                    "azimuth_user": azimuth_user,
                    "azimuth_proposed": azimuth_proposed,
                }

            def rule_check(self, context, calc_vals, data=None):
                return calc_vals["azimuth_user"] == calc_vals["azimuth_proposed"]


# ------------------------
