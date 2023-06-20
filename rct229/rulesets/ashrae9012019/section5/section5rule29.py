from rct229.rule_engine.rule_base import RuleDefinitionBase
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

FAIL_MSG = "Baseline fenestration was modeled with shading projections and/or overhangs, which is incorrect."


class Section5Rule29(RuleDefinitionListIndexedBase):
    """Rule 29 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule29, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule29.BuildingRule(),
            index_rmr="baseline",
            id="5-29",
            description="Baseline fenestration shall be assumed to be flush with the exterior wall, and no shading "
            "projections shall be modeled.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(d) Building Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule29.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule29.BuildingRule.AboveGradeWallRule(),
                index_rmr="baseline",
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data):
            building_b = context.baseline
            return {
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
            }

        def list_filter(self, context_item, data):
            surface_b = context_item.baseline
            return (
                get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL
                and data["scc_dict_b"][surface_b["id"]] != SCC.UNREGULATED
            )

        class AboveGradeWallRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule29.BuildingRule.AboveGradeWallRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    list_path="subsurfaces[*]",
                    each_rule=Section5Rule29.BuildingRule.AboveGradeWallRule.SubsurfaceRule(),
                    index_rmr="baseline",
                )

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule29.BuildingRule.AboveGradeWallRule.SubsurfaceRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                        fail_msg=FAIL_MSG,
                        required_fields={
                            "$": ["has_shading_overhang", "has_shading_sidefins"]
                        },
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.baseline
                    return {
                        "has_shading_overhang": subsurface_b["has_shading_overhang"],
                        "has_shading_sidefins": subsurface_b["has_shading_sidefins"],
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    return not (
                        calc_vals["has_shading_overhang"]
                        or calc_vals["has_shading_sidefins"]
                    )
