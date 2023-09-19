from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)


class Section5Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule7, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule7.BuildingRule(),
            index_rmr="baseline",
            id="5-7",
            description="Baseline below-grade walls shall conform with assemblies detailed in Appendix A Concrete block, A4)",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule7.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule7.BuildingRule.SurfaceRule(),
                index_rmr="baseline",
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
            }

        def list_filter(self, context_item, data):
            surface_b = context_item.baseline
            return get_opaque_surface_type(surface_b) == OST.BELOW_GRADE_WALL

        class SurfaceRule(PartialRuleDefinition):
            def __init__(self):
                super(Section5Rule7.BuildingRule.SurfaceRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.baseline
                surface_conditioning_category_dict = data[
                    "surface_conditioning_category_dict"
                ]
                surface_category = surface_conditioning_category_dict[surface_b["id"]]
                return {
                    "surface_category": surface_category,
                }

            def applicability_check(self, context, calc_vals, data):
                surface_category = calc_vals["surface_category"]
                return surface_category != SCC.UNREGULATED
