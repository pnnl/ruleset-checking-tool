from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
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


class Section5Rule13(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule13, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule13.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-13",
            description="Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design. ",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule13.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={},
                each_rule=Section5Rule13.BuildingRule.UnregulatedSurfaceRule(),
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
            scc = data["surface_conditioning_category_dict"]
            surface_b = context_item.BASELINE_0
            return scc[surface_b["id"]] == SCC.UNREGULATED

        class UnregulatedSurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section5Rule13.BuildingRule.UnregulatedSurfaceRule, self
                ).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={"$": ["construction"]},
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.BASELINE_0
                surface_p = context.PROPOSED

                surface_b_type = get_opaque_surface_type(surface_b)
                surface_b_construction = surface_b["construction"]
                surface_p_type = get_opaque_surface_type(surface_p)
                surface_p_construction = surface_p["construction"]

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
                                surface_b_construction, "construction", "u_factor"
                            ),
                        ),
                        "proposed_surface_u_factor": CalcQ(
                            "thermal_transmittance",
                            getattr_(
                                surface_p_construction, "construction", "u_factor"
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
