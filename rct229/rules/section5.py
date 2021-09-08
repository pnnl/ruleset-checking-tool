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


class Section5Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section5Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule3.BuildingRule(),
            index_rmr="baseline",
            id="5-3",
            description="The building shall be modeled so that it does not shade itself",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule3.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule3.BuildingRule.SurfaceRule(),
                index_rmr="baseline",
                list_path="$..surfaces[*]",  # All surfaces inside the building
            )

        class SurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule3.BuildingRule.SurfaceRule, self,).__init__(
                    required_fields={
                        "$": ["adjacent_to", "does_cast_shade"],
                    },
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def is_applicable(self, context, data=None):
                return context.baseline["adjacent_to"] == "EXTERIOR"

            def get_calc_vals(self, context, data=None):
                return {"does_cast_shade": context.baseline["does_cast_shade"]}

            def rule_check(self, context, calc_vals, data=None):
                return not calc_vals["does_cast_shade"]


# ------------------------
