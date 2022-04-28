from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id
from rct229.ruleset_functions.get_zone_conditioning_category_dict import get_zone_conditioning_category_dict

class Section5Rule48(RuleDefinitionListIndexedBase):
    """Rule 48 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule48, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule48.BuildingRule(),
            index_rmr="baseline",
            id="5-48",
            description="The air leakage rate in unconditioned and unenclosed spaces must be the same the baseline and proposed design.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):  # put it under the "BuildingRule"
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}


    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule48.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$..zones[*]": ["infiltration"],
                    "$..infiltration[*]": ["infiltration_flow_rate"],
                },
            )

        def get_calc_vals(self, context, data=None):
            climate_zone = data["climate_zone"]
            building_b = context.baseline
            building_p = context.proposed

            baseline_zones = find_all("$..zones[*]", context.baseline)
            proposed_zones = find_all("$..zones[*]", context.proposed)


            zone_conditioning_category = get_zone_conditioning_category_dict(climate_zone, building_b)
            print(zone_conditioning_category)

            # baseline_infiltration=0
            # proposed_infiltration=0
            # # This assumes that the surfaces all match
            # matched_baseline_zones = match_lists_by_id(proposed_zones, baseline_zones)
            # proposed_baseline_zone_pairs = zip(proposed_zones, matched_baseline_zones)
            # for (p_zone, b_zone) in proposed_baseline_zone_pairs:
            #     # if b_zone[] in ["UNENCLOSED", "UNCONDITIONED"]:
            #         pass

            # matched_baseline_zones = match_lists_by_id(proposed_zones, baseline_zones)


            # This assumes that the surfaces all match
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

            # return {"baseline_infiltration": baseline_infiltration,
            #         "proposed_infiltration": proposed_infiltration,}
            return None

        def rule_check(self, context, calc_vals, data=None):
            return calc_vals["baseline_infiltration"] == calc_vals["proposed_infiltration"]
