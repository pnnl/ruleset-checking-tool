from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id
from rct229.ruleset_functions.get_zone_conditioning_category_dict import get_zone_conditioning_category_dict
import pprint
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

            baseline_zones = find_all("$..zones[*]", context.baseline)
            proposed_zones = find_all("$..zones[*]", context.proposed)

            zone_conditioning_category = get_zone_conditioning_category_dict(climate_zone, context.baseline)
            b_RMR_zone = context.baseline["building_segments"][0]["zones"]
            for zone_b in b_RMR_zone:
                if zone_conditioning_category[zone_b["id"]] in ["UNENCLOSED", "UNCONDITIONED"]:
                    zone_b_infiltration = zone_b["infiltration"]["infiltration_flow_rate"]

                    zone_p = match_lists_by_id(proposed_zones[0], zone_b, zone_b["id"]) #### can't find "match_data_element" function
                    zone_p_infiltration = zone_p[0]["infiltration"]["infiltration_flow_rate"]

            return {"baseline_infiltration":zone_b_infiltration,
                    "proposed_infiltration": zone_p_infiltration,}

        def rule_check(self, context, calc_vals, data=None):
            return calc_vals["baseline_infiltration"] == calc_vals["proposed_infiltration"]
