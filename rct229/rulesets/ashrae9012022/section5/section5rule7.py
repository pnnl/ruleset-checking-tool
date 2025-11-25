from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.rulesets.ashrae9012022.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_baseline_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
    get_baseline_surface_conditioning_category_dict,
)


class PRM9012022Rule20r05(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2022 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012022Rule20r05, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather", "constructions"],
                "$.ruleset_model_descriptions[*].weather": ["climate_zone"],
            },
            each_rule=PRM9012022Rule20r05.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-7",
            description="Baseline above-grade wall assemblies must conform with assemblies detailed in  Appendix A (Steel-framed A3.3) ",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        rpd_p = context.PROPOSED
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions_b = rpd_b["ruleset_model_descriptions"][0]["constructions"]
        constructions_p = rpd_p["ruleset_model_descriptions"][0]["constructions"]
        return {
            "climate_zone": climate_zone,
            "constructions_b": constructions_b,
            "constructions_p": constructions_p,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012022Rule20r05.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012022Rule20r05.BuildingRule.SurfaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            building_p = context.PROPOSED
            return {
                "surface_conditioning_category_dict": get_baseline_surface_conditioning_category_dict(
                    data["climate_zone"],
                    building_b,
                    data["constructions_b"],
                    building_p,
                    data["constructions_p"],
                ),
            }

        def list_filter(self, context_item, data):
            surface_b = context_item.BASELINE_0
            return get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL

        class SurfaceRule(PartialRuleDefinition):
            def __init__(self):
                super(PRM9012022Rule20r05.BuildingRule.SurfaceRule, self).__init__(
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
