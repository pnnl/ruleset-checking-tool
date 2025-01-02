from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id


class Section5Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule2, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section5Rule2.BuildingRule(),
            index_rmd=PROPOSED,
            id="5-2",
            description="Orientation is the same in user model and proposed model",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(a) Building Envelope Modeling Requirements for the Proposed building",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule2.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={
                    "$.building_segments[*].zones[*].surfaces[*]": ["azimuth"],
                },
            )

        def get_calc_vals(self, context, data=None):
            failing_surface_ids = []
            proposed_surfaces = find_all(
                "$.building_segments[*].zones[*].surfaces[*]", context.PROPOSED
            )
            user_surfaces = find_all(
                "$.building_segments[*].zones[*].surfaces[*]", context.USER
            )

            # This assumes that the surfaces all match
            matched_user_surfaces = match_lists_by_id(proposed_surfaces, user_surfaces)
            proposed_user_surface_pairs = zip(proposed_surfaces, matched_user_surfaces)
            for p_surface, u_surface in proposed_user_surface_pairs:
                if p_surface["azimuth"] != u_surface["azimuth"]:
                    failing_surface_ids.append(p_surface["id"])

            return {"failing_surface_ids": failing_surface_ids}

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failing_surface_ids"]) == 0
