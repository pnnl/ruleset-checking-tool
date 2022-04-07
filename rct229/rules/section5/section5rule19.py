from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all
from rct229.ruleset_functions.get_area_type_window_wall_area_dict import get_area_type_window_wall_area_dict
from rct229.ruleset_functions.get_opaque_surface_type import
from rct229.utils.match_lists import match_lists_by_id


class Section5Rule19(RuleDefinitionListIndexedBase):
    """Rule 19` of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule19, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section5Rule19.BuildingRule(),
            index_rmr="proposed",
            id="5-19",
            description="For building areas not shown in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in the proposed design or 40% of gross above-grade wall area, whichever is smaller.",
            rmr_context="ruleset_model_instances/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule19.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$..zones[*]": ["infiltration"],
                    "$..infiltration[*]": ["modeling_method"],
                    "$..infiltration[*]": ["algorithm_name"],
                },
            )

        def get_calc_vals(self, context, data=None):

            # failing_infiltration_zone_ids = []
            # baseline_zones = find_all("$..zones[*]", context.baseline)
            # proposed_zones = find_all("$..zones[*]", context.proposed)
            #
            # # This assumes that the surfaces all match
            # matched_baseline_zones = match_lists_by_id(proposed_zones, baseline_zones)
            # proposed_baseline_zone_pairs = zip(proposed_zones, matched_baseline_zones)
            # for (p_zone, b_zone) in proposed_baseline_zone_pairs:
            #     # need a method like match object
            #     p_zone_infiltration = p_zone["infiltration"]
            #     # b_zone could be NONE - add a check.
            #     b_zone_infiltration = b_zone["infiltration"]
            #
            #     if (
            #         p_zone_infiltration["algorithm_name"]
            #         != b_zone_infiltration["algorithm_name"]
            #         or p_zone_infiltration["modeling_method"]
            #         != b_zone_infiltration["modeling_method"]
            #     ):
            #         failing_infiltration_zone_ids.append(p_zone["id"])
            #
            # return {"failing_infiltration_zone_ids": failing_infiltration_zone_ids}

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failing_infiltration_zone_ids"]) == 0
