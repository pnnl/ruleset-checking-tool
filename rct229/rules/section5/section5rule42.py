from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id
from rct229.utils.std_comparisons import std_equal


class Section5Rule42(RuleDefinitionListIndexedBase):
    """Rule 42 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule42, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule42.BuildingRule(),
            index_rmr="baseline",
            id="5-42",
            description="The baseline roof surfaces shall be modeled using a solar reflectance of 0.30.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule42.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule42.BuildingRule.UnregulatedSurfaceRule(),
                index_rmr="baseline",
                list_path="$..surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.baseline
            # Merge into the existing data dict
            return {
                **data,
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.baseline

            return data["scc_dict_b"][surface_b["id"]] == SCC.UNREGULATED


        def get_calc_vals(self, context, data=None):
            subsurface_b = context.baseline

            return {"surface_optical_property_b ":, }

        def rule_check(self, context, calc_vals, data=None):
            return (calc_vals["surface_optical_property_b"]["absorptance_solar_exterior "] == 0.7)
