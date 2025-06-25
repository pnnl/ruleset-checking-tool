from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
    SurfaceConditioningCategory as SCC,
)
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.utils.assertions import getattr_, assert_

MANUAL_CHECK_REQUIRED_MSG = (
    "Zone has both residential and non-residential spaces and the construction requirements "
    "for slab-on-grade floor are different. Verify construction is modeled correctly. "
)
FAIL_MSG = (
    'Baseline slab F-factor is not as expected for slabs that are less than 24" below grade. verify that the '
    'slab is more than 24" below grade and is unregulated. '
)


class PRM9012019Rule40d86(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule40d86, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather", "constructions"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule40d86.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-12",
            description="Baseline slab-on-grade floor assemblies must match the appropriate assembly maximum F-factors in Tables G3.4-1 through G3.4-9.",
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
            super(PRM9012019Rule40d86.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={},
                each_rule=PRM9012019Rule40d86.BuildingRule.SlabOnGradeFloorRule(),
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
            construction_id = getattr_(surface_b, "Surface", "construction")
            has_radiant_heat = next(
                (
                    construction.get("has_radiant_heat", False)
                    for construction in data["constructions"]
                    if construction["id"] == construction_id
                )
            )
            scc = data["surface_conditioning_category_dict"][surface_b["id"]]
            return (
                get_opaque_surface_type(surface_b, has_radiant_heat) == OST.UNHEATED_SOG
                and scc is not SCC.UNREGULATED
            )

        class SlabOnGradeFloorRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule40d86.BuildingRule.SlabOnGradeFloorRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={"$": ["construction"]},
                    manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                    fail_msg=FAIL_MSG,
                    precision={
                        "floor_f_factor_b": {
                            "precision": 0.001,
                            "unit": "Btu/(hr*ft*R)",
                        }
                    },
                )

            def get_calc_vals(self, context, data=None):
                climate_zone: str = data["climate_zone"]
                slab_on_grade = context.BASELINE_0
                scc: str = data["surface_conditioning_category_dict"][
                    slab_on_grade["id"]
                ]
                slab_on_grade_f_factor = next(
                    (
                        construction.get("f_factor")
                        for construction in data["constructions"]
                        if construction["id"] == slab_on_grade["construction"]
                    )
                )
                assert_(
                    slab_on_grade_f_factor is not None,
                    f"F-factor for slab on grade construction '{slab_on_grade['construction']}' is missing",
                )

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
                    "slab_on_grade_floor_f_factor": CalcQ(
                        "linear_thermal_transmittance", slab_on_grade_f_factor
                    ),
                    "target_f_factor": CalcQ(
                        "linear_thermal_transmittance", target_f_factor
                    ),
                    "target_f_factor_res": CalcQ(
                        "linear_thermal_transmittance", target_f_factor_res
                    ),
                    "target_f_factor_nonres": CalcQ(
                        "linear_thermal_transmittance", target_f_factor_nonres
                    ),
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                target_f_factor_res = calc_vals["target_f_factor_res"]
                target_f_factor_nonres = calc_vals["target_f_factor_nonres"]

                return target_f_factor_res != target_f_factor_nonres

            def rule_check(self, context, calc_vals=None, data=None):
                target_f_factor = calc_vals["target_f_factor"]
                slab_on_grade_floor_f_factor = calc_vals["slab_on_grade_floor_f_factor"]
                return self.precision_comparison["floor_f_factor_b"](
                    slab_on_grade_floor_f_factor, target_f_factor
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                target_f_factor = calc_vals["target_f_factor"]
                slab_on_grade_floor_f_factor = calc_vals["slab_on_grade_floor_f_factor"]
                return std_equal(
                    std_val=target_f_factor, val=slab_on_grade_floor_f_factor
                )
