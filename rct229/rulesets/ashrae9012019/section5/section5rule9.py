from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
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


class Section5Rule9(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule9, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule9.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-9",
            description="Baseline floor assemblies must conform with assemblies detailed in  Appendix A (Floors—Steel-joist (A5.3))",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule9.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section5Rule9.BuildingRule.SurfaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
            }

        def list_filter(self, context_item, data):
            surface_b = context_item.BASELINE_0
            return get_opaque_surface_type(surface_b) == OST.FLOOR

        class SurfaceRule(PartialRuleDefinition):
            def __init__(self):
                super(Section5Rule9.BuildingRule.SurfaceRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.BASELINE_0
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

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                surface_b = context.BASELINE_0
                surface_id_b = surface_b["id"]

                return f"{surface_id_b} is a regulated floor surface. Conduct a manual check to confirm that Baseline floor assemblies conform with assemblies detailed in Appendix A."
