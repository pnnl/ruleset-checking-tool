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
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal


class PRM9012019Rule73r04(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule73r04, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather", "constructions"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule73r04.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-13",
            description="Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design. ",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        rpd_p = context.PROPOSED
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions_b = rpd_b["ruleset_model_descriptions"][0]["constructions"]
        constructions_p = rpd_p["ruleset_model_descriptions"][0]["constructions"]
        return {
            "climate_zone": climate_zone,
            "constructions_b": constructions_b,
            "constructions_p": constructions_p,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule73r04.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={},
                each_rule=PRM9012019Rule73r04.BuildingRule.UnregulatedSurfaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.BASELINE_0
            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building, data["constructions_b"]
                ),
            }

        def list_filter(self, context_item, data=None):
            scc = data["surface_conditioning_category_dict"]
            surface_b = context_item.BASELINE_0
            return scc[surface_b["id"]] == SCC.UNREGULATED

        class UnregulatedSurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule73r04.BuildingRule.UnregulatedSurfaceRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={"$": ["construction"]},
                    precision={
                        "surface_u_factor_b": {
                            "precision": 0.001,
                            "unit": "Btu/(hr*ft2*R)",
                        },
                        "surface_c_factor_b": {
                            "precision": 0.001,
                            "unit": "Btu/(hr*ft2*R)",
                        },
                        "surface_f_factor_b": {
                            "precision": 0.001,
                            "unit": "Btu/(hr*ft*R)",
                        },
                    },
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.BASELINE_0
                surface_p = context.PROPOSED

                construction_id_b = getattr_(surface_b, "Surface", "construction")
                construction_id_p = getattr_(surface_p, "Surface", "construction")

                surface_b_construction = next(
                    (
                        construction
                        for construction in data["constructions_b"]
                        if construction["id"] == construction_id_b
                    )
                )
                surface_p_construction = next(
                    (
                        construction
                        for construction in data["constructions_p"]
                        if construction["id"] == construction_id_p
                    )
                )

                has_radiant_heat_b = surface_b_construction.get(
                    "has_radiant_heat", False
                )
                has_radiant_heat_p = surface_p_construction.get(
                    "has_radiant_heat", False
                )

                surface_b_type = get_opaque_surface_type(surface_b, has_radiant_heat_b)
                surface_p_type = get_opaque_surface_type(surface_p, has_radiant_heat_p)

                calc_vals = {
                    "baseline_surface_type": surface_b_type,
                    "proposed_surface_type": surface_p_type,
                }

                if surface_b_type in [OST.ABOVE_GRADE_WALL, OST.FLOOR, OST.ROOF]:
                    return {
                        **calc_vals,
                        "baseline_surface_u_factor": CalcQ(
                            "thermal_transmittance",
                            getattr_(
                                surface_b_construction, "Construction", "u_factor"
                            ),
                        ),
                        "proposed_surface_u_factor": CalcQ(
                            "thermal_transmittance",
                            getattr_(
                                surface_p_construction, "Construction", "u_factor"
                            ),
                        ),
                    }
                elif surface_b_type in [OST.UNHEATED_SOG, OST.HEATED_SOG]:
                    return {
                        **calc_vals,
                        "baseline_surface_f_factor": CalcQ(
                            "linear_thermal_transmittance",
                            getattr_(
                                surface_b_construction, "construction", "f_factor"
                            ),
                        ),
                        "proposed_surface_f_factor": CalcQ(
                            "linear_thermal_transmittance",
                            getattr_(
                                surface_p_construction, "construction", "f_factor"
                            ),
                        ),
                    }
                elif surface_b_type == OST.BELOW_GRADE_WALL:
                    return {
                        **calc_vals,
                        "baseline_surface_c_factor": CalcQ(
                            "thermal_transmittance",
                            getattr_(
                                surface_b_construction, "construction", "c_factor"
                            ),
                        ),
                        "proposed_surface_c_factor": CalcQ(
                            "thermal_transmittance",
                            getattr_(
                                surface_p_construction, "construction", "c_factor"
                            ),
                        ),
                    }
                else:
                    # Will never reach this line
                    # The OST defaults all unidentifiable surfaces to above wall grade
                    # Serve code completeness
                    raise Exception(f"Unrecognized surface type: {surface_b_type}")

            def rule_check(self, context, calc_vals=None, data=None):
                baseline_surface_type = calc_vals["baseline_surface_type"]
                proposed_surface_type = calc_vals["proposed_surface_type"]
                # Check 1. surface type needs to be matched
                if (
                    proposed_surface_type is None
                    or baseline_surface_type != proposed_surface_type
                ):
                    return False

                if baseline_surface_type in [OST.ABOVE_GRADE_WALL, OST.FLOOR, OST.ROOF]:
                    return self.precision_comparison["surface_u_factor_b"](
                        calc_vals["baseline_surface_u_factor"],
                        calc_vals["proposed_surface_u_factor"],
                    )

                elif baseline_surface_type in [OST.UNHEATED_SOG, OST.HEATED_SOG]:
                    return self.precision_comparison["surface_f_factor_b"](
                        calc_vals["baseline_surface_f_factor"],
                        calc_vals["proposed_surface_f_factor"],
                    )

                elif baseline_surface_type == OST.BELOW_GRADE_WALL:

                    return self.precision_comparison["surface_c_factor_b"](
                        calc_vals["baseline_surface_c_factor"],
                        calc_vals["proposed_surface_c_factor"],
                    )
                else:
                    return False

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                baseline_surface_type = calc_vals["baseline_surface_type"]
                proposed_surface_type = calc_vals["proposed_surface_type"]
                # Check 1. surface type needs to be matched
                if (
                    proposed_surface_type is None
                    or baseline_surface_type != proposed_surface_type
                ):
                    return False

                if baseline_surface_type in [OST.ABOVE_GRADE_WALL, OST.FLOOR, OST.ROOF]:
                    return std_equal(
                        calc_vals["baseline_surface_u_factor"],
                        calc_vals["proposed_surface_u_factor"],
                    )

                elif baseline_surface_type in [OST.UNHEATED_SOG, OST.HEATED_SOG]:
                    return std_equal(
                        calc_vals["baseline_surface_f_factor"],
                        calc_vals["proposed_surface_f_factor"],
                    )

                elif baseline_surface_type == OST.BELOW_GRADE_WALL:
                    return std_equal(
                        calc_vals["baseline_surface_c_factor"],
                        calc_vals["proposed_surface_c_factor"],
                    )
                else:
                    return False
