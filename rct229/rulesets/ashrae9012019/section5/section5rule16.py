from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_area_type_window_wall_area_dict import (
    get_area_type_window_wall_area_dict,
)
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
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
FAIL_MSG = (
    "The vertical fenestration is not distributed across baseline opaque surfaces "
    "in the same proportion as in the proposed design. Verify if envelope is existing "
    "or altered and can be excluded from this check."
)


def _calc_surface_fenestration(surface: dict):
    total = ZERO.AREA
    for subsurface in surface.get("subsurfaces", []):
        classification = getattr_(subsurface, "subsurface", "classification")

        glazed = subsurface.get("glazed_area", ZERO.AREA)
        opaque = subsurface.get("opaque_area", ZERO.AREA)

        if classification == DOOR:
            if glazed > opaque:
                total += glazed + opaque
        else:
            total += glazed + opaque

    return total


class PRM9012019Rule80o45(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super().__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule80o45.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-16",
            description="The vertical fenestration shall be distributed on each face of the building in the same proportion as in the proposed design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "$.ruleset_model_descriptions[*].weather": ["climate_zone"],
            },
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        rmd_b = rpd_b["ruleset_model_descriptions"][0]

        return {
            "climate_zone": rmd_b["weather"]["climate_zone"],
            "constructions": rmd_b.get("constructions"),
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super().__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule80o45.BuildingRule.AboveGradeWallRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            building_p = context.PROPOSED
            climate_zone = data["climate_zone"]
            constructions = data["constructions"]
            surface_conditioning_category_dict_b = (
                get_surface_conditioning_category_dict(
                    climate_zone, building_b, constructions, BASELINE_0
                )
            )
            window_wall_b = get_area_type_window_wall_area_dict(
                climate_zone,
                constructions,
                building_b,
                BASELINE_0,
                surface_conditioning_category_dict_b,
            )
            window_wall_p = get_area_type_window_wall_area_dict(
                climate_zone, constructions, building_p, PROPOSED
            )

            # Cache per-surface fenestration area (baseline + proposed)
            surface_fenestration_b = {}
            surface_fenestration_p = {}

            for segment in building_b.get("building_segments", []):
                for zone in segment.get("zones", []):
                    for surface in zone.get("surfaces", []):
                        surface_fenestration_b[
                            surface["id"]
                        ] = _calc_surface_fenestration(surface)

            for segment in building_p.get("building_segments", []):
                for zone in segment.get("zones", []):
                    for surface in zone.get("surfaces", []):
                        surface_fenestration_p[
                            surface["id"]
                        ] = _calc_surface_fenestration(surface)

            return {
                "total_fenestration_area_b": sum(
                    (
                        v.get("total_window_area", ZERO.AREA)
                        for v in window_wall_b.values()
                    ),
                    ZERO.AREA,
                ),
                "total_fenestration_area_p": sum(
                    (
                        v.get("total_window_area", ZERO.AREA)
                        for v in window_wall_p.values()
                    ),
                    ZERO.AREA,
                ),
                "surface_fenestration_b": surface_fenestration_b,
                "surface_fenestration_p": surface_fenestration_p,
                "surface_conditioning_category_dict_b": surface_conditioning_category_dict_b,
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            return (
                get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL
                and data["surface_conditioning_category_dict_b"][surface_b["id"]]
                != SCC.UNREGULATED
            )

        class AboveGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule80o45.BuildingRule.AboveGradeWallRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["construction"],
                    },
                    precision={
                        "total_fenestration_area_surface_b / total_fenstration_area_b": {
                            "precision": 0.01,
                            "unit": "",
                        }
                    },
                    fail_msg=FAIL_MSG,
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.BASELINE_0
                surface_p = context.PROPOSED

                return {
                    "total_fenestration_area_surface_b": CalcQ(
                        "area", data["surface_fenestration_b"][surface_b["id"]]
                    ),
                    "total_fenestration_area_b": CalcQ(
                        "area", data["total_fenestration_area_b"]
                    ),
                    "total_fenestration_area_surface_p": CalcQ(
                        "area", data["surface_fenestration_p"][surface_p["id"]]
                    ),
                    "total_fenestration_area_p": CalcQ(
                        "area", data["total_fenestration_area_p"]
                    ),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                b_surf = calc_vals["total_fenestration_area_surface_b"]
                p_surf = calc_vals["total_fenestration_area_surface_p"]
                b_tot = calc_vals["total_fenestration_area_b"]
                p_tot = calc_vals["total_fenestration_area_p"]

                return (
                    b_tot == ZERO.AREA and p_tot == ZERO.AREA
                ) or self.precision_comparison[
                    "total_fenestration_area_surface_b / total_fenstration_area_b"
                ](
                    (b_surf / b_tot).magnitude,
                    (p_surf / p_tot).magnitude,
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                b_surf = calc_vals["total_fenestration_area_surface_b"]
                p_surf = calc_vals["total_fenestration_area_surface_p"]
                b_tot = calc_vals["total_fenestration_area_b"]
                p_tot = calc_vals["total_fenestration_area_p"]

                return (b_tot == ZERO.AREA and p_tot == ZERO.AREA) or std_equal(
                    (b_surf / b_tot).magnitude,
                    (p_surf / p_tot).magnitude,
                )
