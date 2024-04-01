from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
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
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal


class Section5Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule6, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section5Rule6.BuildingRule(),
            index_rmr=BASELINE_0,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            id="5-6",
            description="Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Table G3.4-1 through G3.4-8.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule6.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={},
                each_rule=Section5Rule6.BuildingRule.BelowGradeWallRule(),
                index_rmr=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.BASELINE_0
            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            scc = data["surface_conditioning_category_dict"][surface_b["id"]]
            return (
                get_opaque_surface_type(surface_b) == OST.BELOW_GRADE_WALL
                and scc is not SCC.UNREGULATED
            )

        class BelowGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule6.BuildingRule.BelowGradeWallRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["construction"],
                        "construction": ["c_factor"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                below_grade_wall = context.BASELINE_0
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
                    target_c_factor = table_G34_lookup(
                        climate_zone, scc, OST.BELOW_GRADE_WALL
                    )["c_factor"]
                elif scc == SCC.EXTERIOR_MIXED:
                    target_c_factor_res = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_RESIDENTIAL, OST.BELOW_GRADE_WALL
                    )["c_factor"]
                    target_c_factor_nonres = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_NON_RESIDENTIAL, OST.BELOW_GRADE_WALL
                    )["c_factor"]

                    if target_c_factor_res == target_c_factor_nonres:
                        target_c_factor = target_c_factor_res

                return {
                    "below_grade_wall_c_factor": CalcQ(
                        "thermal_transmittance", wall_c_factor
                    ),
                    "target_c_factor": CalcQ("thermal_transmittance", target_c_factor),
                    "target_c_factor_res": CalcQ(
                        "thermal_transmittance", target_c_factor_res
                    ),
                    "target_c_factor_nonres": CalcQ(
                        "thermal_transmittance", target_c_factor_nonres
                    ),
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                target_c_factor_res = calc_vals["target_c_factor_res"]
                target_c_factor_nonres = calc_vals["target_c_factor_nonres"]
                return (
                    target_c_factor_res is not None
                    and target_c_factor_nonres is not None
                    and target_c_factor_res != target_c_factor_nonres
                )

            def rule_check(self, context, calc_vals=None, data=None):
                below_grade_wall_c_factor = calc_vals["below_grade_wall_c_factor"]
                target_c_factor = calc_vals["target_c_factor"]

                return std_equal(val=below_grade_wall_c_factor, std_val=target_c_factor)
