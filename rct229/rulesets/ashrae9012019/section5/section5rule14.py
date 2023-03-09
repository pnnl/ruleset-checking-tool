from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (get_opaque_surface_type, OpaqueSurfaceType as OST)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import \
    get_surface_conditioning_category_dict


class Section5Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule14, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule14.BuildingRule(),
            index_rmr="baseline",
            id="5-12",
            description=" Baseline slab-on-grade assemblies must conform with assemblies detailed in Appendix A (Unheated Slabs A6).",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule14.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={"$": "building_segments"},
                each_rule=Section5Rule14.BuildingRule.SurfaceRule(),
                index_rmr="baseline",
                list_path="$..surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.baseline
            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        def list_filter(self, context_item, data):
            surface = context_item.baseline
            return get_opaque_surface_type(surface) in [OST.HEATED_SOG, OST.UNHEATED_SOG]

        class SurfaceRule(PartialRuleDefinition):
            def __init__(self):
                super(Section5Rule14.BuildingRule.SurfaceRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    required_fields={},
                )

            def get_calc_vals(self, context, data=None):
                surface = context.baseline
                surface_conditioning_category_dict = data["surface_conditioning_category_dict"]
                surface_category = surface_conditioning_category_dict[surface["id"]]
                surface_type = get_opaque_surface_type(surface)
                return {
                    "surface_category": surface_category,
                    "surface_type": surface_type
                }

            def applicability_check(self, context, calc_vals, data):
                surface_category = calc_vals["surface_category"]
                return surface_category != "UNREGULATED"
