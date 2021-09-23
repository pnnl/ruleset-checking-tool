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

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule3.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$..surfaces[*]": ["adjacent_to"],
                    "$..surfaces[?(@.adjacent_to='EXTERIOR')]": ["does_cast_shade"],
                },
            )

        def get_calc_vals(self, context, data=None):
            baseline_surfaces_casting_shade_ids = []
            for surface in find_all(
                "$..surfaces[?(@.adjacent_to='EXTERIOR')]", context.baseline
            ):
                if surface["does_cast_shade"]:
                    baseline_surfaces_casting_shade_ids.append(surface["id"])

            return {
                "baseline_surfaces_casting_shade_ids": baseline_surfaces_casting_shade_ids
            }

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["baseline_surfaces_casting_shade_ids"]) == 0


# ------------------------
