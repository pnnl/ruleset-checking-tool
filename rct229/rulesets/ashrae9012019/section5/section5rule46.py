from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id


class Section5Rule46(RuleDefinitionListIndexedBase):
    """Rule 46 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule46, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section5Rule46.BuildingRule(),
            index_rmr="proposed",
            id="5-46",
            description="The infiltration shall be modeled using the same methodology and adjustments for weather and building operation in both the proposed design and the baseline building design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule46.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$.building_segments[*].zones[*]": ["infiltration"],
                    "$.building_segments[*].zones[*].infiltration": [
                        "algorithm_name",
                        "modeling_method",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            failing_infiltration_zone_ids = []
            baseline_zones = find_all(
                "$.building_segments[*].zones[*]", context.baseline
            )
            proposed_zones = find_all(
                "$.building_segments[*].zones[*]", context.proposed
            )

            # This assumes that the surfaces all match
            matched_baseline_zones = match_lists_by_id(proposed_zones, baseline_zones)
            proposed_baseline_zone_pairs = zip(proposed_zones, matched_baseline_zones)
            for p_zone, b_zone in proposed_baseline_zone_pairs:
                # need a method like match object
                p_zone_infiltration = p_zone["infiltration"]
                # b_zone could be NONE - add a check.
                b_zone_infiltration = b_zone["infiltration"]

                if (
                    p_zone_infiltration["algorithm_name"]
                    != b_zone_infiltration["algorithm_name"]
                    or p_zone_infiltration["modeling_method"]
                    != b_zone_infiltration["modeling_method"]
                ):
                    failing_infiltration_zone_ids.append(p_zone["id"])

            return {"failing_infiltration_zone_ids": failing_infiltration_zone_ids}

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failing_infiltration_zone_ids"]) == 0
