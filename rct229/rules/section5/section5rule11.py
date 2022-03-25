from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType,
    # BELOW_GRADE_WALL,
    # ABOVE_GRADE_WALL,
    get_opaque_surface_type,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory,
    # EXTERIOR_MIXED,
    # EXTERIOR_NON_RESIDENTIAL,
    # EXTERIOR_RESIDENTIAL,
    # SEMI_EXTERIOR,
    # UNREGULATED,
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all


class Section5Rule11(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule11, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule11.BuildingRule(),
            index_rmr="baseline",
            id="5-11",
            description="Baseline above-grade wall assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8.",
            list_path="buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule11.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={},
                each_rule=Section5Rule11.BuildingRule.AboveGradeWallRule(),
                index_rmr="baseline",
            )

        def create_context_list(self, context, data=None):
            building = context.baseline
            # List of all baseline above-grade wall surfaces to become the context for AboveGradeWallRule
            return [
                UserBaselineProposedVals(None, surface, None)
                for surface in find_all("$..surfaces[*]", building)
                if get_opaque_surface_type(surface) == OpaqueSurfaceType.ABOVE_GRADE_WALL
            ]

        def create_data(self, context, data=None):
            building = context.baseline
            # Merge into the existing data dict
            return {
                **data,
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        class AboveGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule11.BuildingRule.AboveGradeWallRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    required_fields={},
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                above_grade_wall = context.baseline
                scc: str = data["surface_conditioning_category_dict"][above_grade_wall["id"]]
                above_grade_wall_u_factor = above_grade_wall["construction"]["u_factor"]
                print(f"scc: {scc}")
                target_u_factor = None
                target_u_factor_res = None
                target_u_factor_nonres = None

                if scc in [
                    SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
                    SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
                    SurfaceConditioningCategory.SEMI_EXTERIOR,
                ]:
                    target_u_factor = table_G34_lookup(climate_zone, scc, OpaqueSurfaceType.ABOVE_GRADE_WALL)[
                        "u_value"
                    ]
                elif scc == SurfaceConditioningCategory.EXTERIOR_MIXED:
                    target_u_factor_res = table_G34_lookup(
                        climate_zone, SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL, OpaqueSurfaceType.ABOVE_GRADE_WALL
                    )["u_value"]
                    target_u_factor_nonres = table_G34_lookup(
                        climate_zone, SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL, OpaqueSurfaceType.ABOVE_GRADE_WALL
                    )["u_value"]
                    if target_u_factor_res == target_u_factor_nonres:
                        target_u_factor = target_u_factor_res

                return {
                    "above_grade_wall_u_factor": above_grade_wall_u_factor,
                    "target_u_factor": target_u_factor,
                    "target_u_factor_res": target_u_factor_res,
                    "target_u_factor_nonres": target_u_factor_nonres,
                }

            def manaul_check_required(self, context, calc_vals, data=None):
                target_u_factor_res = calc_vals["target_u_factor_res"]
                target_u_factor_nonres = calc_vals["target_u_factor_nonres"]

                return (
                    target_u_factor_res is not None
                    and target_u_factor_nonres is not None
                    and target_u_factor_res != target_u_factor_nonres
                )

            def rule_check(self, context, calc_vals, data=None):
                above_grade_wall_u_factor = calc_vals["above_grade_wall_u_factor"]
                target_u_factor = calc_vals["target_u_factor"]

                return above_grade_wall_u_factor == target_u_factor
