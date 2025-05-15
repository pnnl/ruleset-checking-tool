from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id


class PRM9012019Rule69u47(RuleDefinitionListIndexedBase):
    """Rule 34 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule69u47, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule69u47.BuildingRule(),
            index_rmd=PROPOSED,
            id="5-34",
            description="The infiltration shall be modeled using the same methodology and adjustments for weather and building operation in both the proposed design and the baseline building design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule69u47.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
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
                "$.building_segments[*].zones[*]", context.BASELINE_0
            )
            proposed_zones = find_all(
                "$.building_segments[*].zones[*]", context.PROPOSED
            )

            # This assumes that the surfaces all match
            matched_baseline_zones = match_lists_by_id(proposed_zones, baseline_zones)

            assert_(
                None not in matched_baseline_zones,
                "The 'zones' objects between baseline and proposed don't match.",
            )

            proposed_baseline_zone_pairs = zip(proposed_zones, matched_baseline_zones)

            for p_zone, b_zone in proposed_baseline_zone_pairs:
                # need a method like match object
                p_zone_infiltration = p_zone["infiltration"]
                b_zone_infiltration = b_zone["infiltration"]

                if (
                    p_zone_infiltration["algorithm_name"]
                    != b_zone_infiltration["algorithm_name"]
                    or p_zone_infiltration["modeling_method"]
                    != b_zone_infiltration["modeling_method"]
                ):
                    failing_infiltration_zone_ids.append(p_zone["id"])

            return {"failing_infiltration_zone_ids": failing_infiltration_zone_ids}

        def rule_check(self, context, calc_vals=None, data=None):
            return not calc_vals["failing_infiltration_zone_ids"]
