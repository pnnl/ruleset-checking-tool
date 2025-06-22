from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
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
from rct229.utils.assertions import assert_


class PRM9012019Rule48v87(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule48v87, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather", "constructions"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule48v87.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-8",
            description="Baseline above-grade wall assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_b["ruleset_model_descriptions"][0]["constructions"]
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule48v87.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={},
                each_rule=PRM9012019Rule48v87.BuildingRule.AboveGradeWallRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.BASELINE_0
            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building, data["constructions"]
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            scc = data["surface_conditioning_category_dict"][surface_b["id"]]
            return (
                get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL
                and scc is not SCC.UNREGULATED
            )

        class AboveGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule48v87.BuildingRule.AboveGradeWallRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["construction"],
                    },
                    precision={
                        "ag_wall_u_factor_b": {
                            "precision": 0.001,
                            "unit": "Btu/(hr*ft2*R)",
                        }
                    },
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                constructions = data["constructions"]
                above_grade_wall = context.BASELINE_0
                scc: str = data["surface_conditioning_category_dict"][
                    above_grade_wall["id"]
                ]
                wall_u_factor = next(
                    (
                        construction.get("u_factor")
                        for construction in constructions
                        if construction["id"] == above_grade_wall["construction"]
                    )
                )
                assert_(
                    wall_u_factor is not None,
                    f"U-factor for above grade wall construction '{above_grade_wall['construction']}' is missing",
                )

                target_u_factor = None
                target_u_factor_res = None
                target_u_factor_nonres = None

                if scc in [
                    SCC.EXTERIOR_RESIDENTIAL,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    SCC.SEMI_EXTERIOR,
                ]:
                    target_u_factor = table_G34_lookup(
                        climate_zone, scc, OST.ABOVE_GRADE_WALL
                    )["u_value"]
                elif scc == SCC.EXTERIOR_MIXED:
                    target_u_factor_res = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_RESIDENTIAL, OST.ABOVE_GRADE_WALL
                    )["u_value"]
                    target_u_factor_nonres = table_G34_lookup(
                        climate_zone, SCC.EXTERIOR_NON_RESIDENTIAL, OST.ABOVE_GRADE_WALL
                    )["u_value"]
                    if target_u_factor_res == target_u_factor_nonres:
                        target_u_factor = target_u_factor_res

                return {
                    "above_grade_wall_u_factor": CalcQ(
                        "thermal_transmittance", wall_u_factor
                    ),
                    "target_u_factor": CalcQ("thermal_transmittance", target_u_factor),
                    "target_u_factor_res": CalcQ(
                        "thermal_transmittance", target_u_factor_res
                    ),
                    "target_u_factor_nonres": CalcQ(
                        "thermal_transmittance", target_u_factor_nonres
                    ),
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                target_u_factor_res = calc_vals["target_u_factor_res"]
                target_u_factor_nonres = calc_vals["target_u_factor_nonres"]

                return target_u_factor_res != target_u_factor_nonres

            def rule_check(self, context, calc_vals=None, data=None):
                return self.precision_comparison["ag_wall_u_factor_b"](
                    calc_vals["above_grade_wall_u_factor"], calc_vals["target_u_factor"]
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                above_grade_wall_u_factor = calc_vals["above_grade_wall_u_factor"]
                target_u_factor = calc_vals["target_u_factor"]
                return std_equal(target_u_factor, above_grade_wall_u_factor)
