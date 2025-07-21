from rct229.rule_engine.rule_base import RuleDefinitionBase
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
from rct229.utils.pint_utils import ZERO

FAIL_MSG = "Baseline fenestration was modeled with shading projections and/or overhangs, which is incorrect."


class PRM9012019Rule50p59(RuleDefinitionListIndexedBase):
    """Rule 22 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule50p59, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule50p59.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-22",
            description="Baseline fenestration shall be assumed to be flush with the exterior wall, and no shading "
            "projections shall be modeled.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(d) Building Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_b["ruleset_model_descriptions"][0].get("constructions")
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule50p59.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule50p59.BuildingRule.AboveGradeWallRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data):
            building_b = context.BASELINE_0
            return {
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b, data["constructions"]
                ),
            }

        def list_filter(self, context_item, data):
            surface_b = context_item.BASELINE_0
            return (
                get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL
                and data["scc_dict_b"][surface_b["id"]] != SCC.UNREGULATED
                and len(surface_b.get("subsurfaces", [])) > 0
            )

        class AboveGradeWallRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule50p59.BuildingRule.AboveGradeWallRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    list_path="subsurfaces[*]",
                    each_rule=PRM9012019Rule50p59.BuildingRule.AboveGradeWallRule.SubsurfaceRule(),
                    index_rmd=BASELINE_0,
                )

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        PRM9012019Rule50p59.BuildingRule.AboveGradeWallRule.SubsurfaceRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                        fail_msg=FAIL_MSG,
                        required_fields={
                            "$": ["has_shading_overhang", "has_shading_sidefins"]
                        },
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.BASELINE_0
                    return {
                        "has_shading_overhang": subsurface_b["has_shading_overhang"],
                        "has_shading_sidefins": subsurface_b["has_shading_sidefins"],
                        "depth_of_overhang": subsurface_b.get("depth_of_overhang"),
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    has_shading_overhang_b = calc_vals["has_shading_overhang"]
                    depth_of_overhang_b = calc_vals["depth_of_overhang"]
                    has_shading_sidefins_b = calc_vals["has_shading_sidefins"]
                    return (
                        has_shading_overhang_b is False
                        or depth_of_overhang_b == ZERO.LENGTH
                    ) and has_shading_sidefins_b is False
