from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal


class Section5Rule8(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule8, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule8.BuildingRule(),
            index_rmr="baseline",
            list_path="ruleset_model_instances[0].buildings[*]",
            id="5-8",
            description="Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Table G3.4-1 through G3.4-8.",
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
        )

    def create_data(self, context, data=None):
        return {"climate_zone": context.baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule8.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={},
                each_rule=Section5Rule8.BuildingRule.BelowGradeWallRule(),
                index_rmr="baseline",
            )

        def create_context_list(self, context, data=None):
            building = context.baseline
            # List of all baseline roof surfaces to become the context for RoofRule
            return [
                UserBaselineProposedVals(None, surface, None)
                for surface in find_all("$..surfaces[*]", building)
                if get_opaque_surface_type(surface) == OST.BELOW_GRADE_WALL
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

        class BelowGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule8.BuildingRule.BelowGradeWallRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    required_fields={
                        "$": ["construction"],
                        "construction": ["c_factor"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                below_grade_wall = context.baseline
                scc: str = data["surface_conditioning_category_dict"][
                    below_grade_wall["id"]
                ]
                wall_c_factor = below_grade_wall["construction"]["c_factor"]

                target_c_factor = None
                target_c_factor_res = None
                target_c_factor_nonres = None

                if scc in [
                    SCC.SEMI_EXTERIOR,
                    SCC.EXTERIOR_RESIDENTIAL,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                ]:
                    target = table_G34_lookup(climate_zone, scc, OST.BELOW_GRADE_WALL)
                    target_c_factor = target["c_factor"]
                elif scc == SCC.EXTERIOR_MIXED:
                    target_c_factor_res = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_RESIDENTIAL, OST.BELOW_GRADE_WALL
                    )
                    target_c_factor_nonres = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_NON_RESIDENTIAL, OST.BELOW_GRADE_WALL
                    )

                    if target_c_factor_res == target_c_factor_nonres:
                        target_c_factor = target_c_factor_res

                return {
                    "below_grade_wall_c_factor": wall_c_factor,
                    "target_c_factor": target_c_factor,
                    "target_c_factor_res": target_c_factor_res,
                    "target_c_factor_nonres": target_c_factor_nonres,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                target_c_factor_res = calc_vals["target_c_factor_res"]
                target_c_factor_nonres = calc_vals["target_c_factor_nonres"]
                return (
                    target_c_factor_res is not None
                    and target_c_factor_nonres is not None
                    and target_c_factor_res != target_c_factor_nonres
                )

            def rule_check(self, context, calc_vals, data=None):
                below_grade_wall_c_factor = calc_vals["below_grade_wall_c_factor"]
                target_c_factor = calc_vals["target_c_factor"]

                return std_equal(below_grade_wall_c_factor, target_c_factor)
