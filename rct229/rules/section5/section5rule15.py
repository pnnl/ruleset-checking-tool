from rct229.data.schema_enums import schema_enums
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
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal


class Section5Rule15(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule15, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule15.BuildingRule(),
            index_rmr="baseline",
            id="5-15",
            description="Baseline slab-on-grade floor assemblies must match the appropriate assembly maximum F-factors in Tables G3.4-1 through G3.4-9.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule15.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={},
                each_rule=Section5Rule15.BuildingRule.SlabOnGradeFloorRule(),
                index_rmr="baseline",
            )

        def create_context_list(self, context, data=None):
            building = context.baseline
            # List of all baseline slab on grade floor surfaces to become the context for SlabOnGradeFloorRule
            return [
                UserBaselineProposedVals(None, surface, None)
                for surface in find_all("$..surfaces[*]", building)
                if get_opaque_surface_type(surface) == OST.UNHEATED_SOG
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

        class SlabOnGradeFloorRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule15.BuildingRule.SlabOnGradeFloorRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    required_fields={
                        "$": ["construction"],
                        "construction": ["f_factor"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                slab_on_grade_floor = context.baseline
                scc: str = data["surface_conditioning_category_dict"][
                    slab_on_grade_floor["id"]
                ]
                slab_on_grade_floor_f_factor = slab_on_grade_floor["construction"][
                    "f_factor"
                ]

                target_f_factor = None
                target_f_factor_res = None
                target_f_factor_nonres = None

                if scc in [
                    SCC.EXTERIOR_RESIDENTIAL,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    SCC.SEMI_EXTERIOR,
                ]:
                    target_f_factor = table_G34_lookup(
                        climate_zone, scc, OST.UNHEATED_SOG
                    )["f_factor"]
                elif scc == SCC.EXTERIOR_MIXED:
                    target_f_factor_res = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_RESIDENTIAL, OST.UNHEATED_SOG
                    )["f_factor"]
                    target_f_factor_nonres = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_NON_RESIDENTIAL, OST.UNHEATED_SOG
                    )["f_factor"]
                    if target_f_factor_res == target_f_factor_nonres:
                        target_f_factor = target_f_factor_res

                return {
                    "slab_on_grade_floor_f_factor": slab_on_grade_floor_f_factor,
                    "target_f_factor": target_f_factor,
                    "target_f_factor_res": target_f_factor_res,
                    "target_f_factor_nonres": target_f_factor_nonres,
                }

            def manaul_check_required(self, context, calc_vals, data=None):
                target_f_factor_res = calc_vals["target_f_factor_res"]
                target_f_factor_nonres = calc_vals["target_f_factor_nonres"]

                return target_f_factor_res != target_f_factor_nonres

            def rule_check(self, context, calc_vals, data=None):
                target_f_factor = calc_vals["target_f_factor"]
                slab_on_grade_floor_f_factor = calc_vals["slab_on_grade_floor_f_factor"]

                return std_equal(target_f_factor, slab_on_grade_floor_f_factor)
