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


class Section5Rule13(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule13, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule13.BuildingRule(),
            index_rmr="baseline",
            id="5-13",
            description="Baseline floor assemblies must  match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-9.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule13.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={"$..zones[*]": ["surfaces"]},
                each_rule=Section5Rule13.BuildingRule.FloorRule(),
                index_rmr="baseline",
            )

        def create_context_list(self, context, data=None):
            building = context.baseline
            # List of all baseline floor surfaces to become the context for RoofRule
            return [
                UserBaselineProposedVals(None, surface, None)
                for surface in find_all("$..surfaces[*]", building)
                if get_opaque_surface_type(surface) == OST.FLOOR
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

        class FloorRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule13.BuildingRule.FloorRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    required_fields={
                        "$": ["construction"],
                        "construction": ["u_factor"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                floor = context.baseline
                scc: str = data["surface_conditioning_category_dict"][floor["id"]]
                floor_u_factor = floor["construction"]["u_factor"]

                target_u_factor = None
                target_u_factor_res = None
                target_u_factor_nonres = None

                if scc in [
                    SCC.EXTERIOR_RESIDENTIAL,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    SCC.SEMI_EXTERIOR,
                ]:
                    target_u_factor = table_G34_lookup(climate_zone, scc, OST.FLOOR)[
                        "u_value"
                    ]
                elif scc == SCC.EXTERIOR_MIXED:
                    target_u_factor_res = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_RESIDENTIAL, OST.FLOOR
                    )["u_value"]
                    target_u_factor_nonres = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_NON_RESIDENTIAL, OST.FLOOR
                    )["u_value"]
                    if target_u_factor_res == target_u_factor_nonres:
                        target_u_factor = target_u_factor_res

                return {
                    "floor_u_factor": floor_u_factor,
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
                floor_u_factor = calc_vals["floor_u_factor"]
                target_u_factor = calc_vals["target_u_factor"]

                return std_equal(floor_u_factor, target_u_factor)
