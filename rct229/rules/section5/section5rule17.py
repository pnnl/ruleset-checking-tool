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
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id
from rct229.utils.std_comparisons import std_equal


class Section5Rule17(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule17, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule17.BuildingRule(),
            index_rmr="baseline",
            id="5-17",
            description="Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design. ",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule17.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={},
                each_rule=Section5Rule17.BuildingRule.UnregulatedSurfaceRule(),
                index_rmr="baseline",
            )

        def create_data(self, context, data=None):
            building = context.baseline
            # Merge into the existing data dict
            return {
                **data,
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        def create_context_list(self, context, data=None):
            # List of all baseline unregulated surfaces to become the context for Unregulated Surfaces
            scc = data["surface_conditioning_category_dict"]

            baseline_surfaces = find_all("$..surfaces[*]", context.baseline)
            proposed_surfaces = find_all("$..surfaces[*]", context.proposed)

            # This assumes that the surfaces matched by IDs between proposed and baseline
            matched_proposed_surfaces = match_lists_by_id(
                baseline_surfaces, proposed_surfaces
            )

            proposed_baseline_surface_pairs = zip(
                baseline_surfaces, matched_proposed_surfaces
            )

            return [
                UserBaselineProposedVals(None, surface_b, surface_p)
                for surface_b, surface_p in proposed_baseline_surface_pairs
                if scc[surface_b["id"]] == SCC.UNREGULATED
            ]

        class UnregulatedSurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section5Rule17.BuildingRule.UnregulatedSurfaceRule, self
                ).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={"$": ["construction"]},
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.baseline
                surface_p = context.proposed

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
                        "baseline_surface_u_factor": getattr_(
                            surface_b_construction, "construction", "u_factor"
                        ),
                        "proposed_surface_u_factor": getattr_(
                            surface_p_construction, "construction", "u_factor"
                        ),
                    }
                elif surface_b_type in [OST.UNHEATED_SOG, OST.HEATED_SOG]:
                    return {
                        **calc_vals,
                        "baseline_surface_f_factor": getattr_(
                            surface_b_construction, "construction", "f_factor"
                        ),
                        "proposed_surface_f_factor": getattr_(
                            surface_p_construction, "construction", "f_factor"
                        ),
                    }
                elif surface_b_type == OST.BELOW_GRADE_WALL:
                    return {
                        **calc_vals,
                        "baseline_surface_c_factor": getattr_(
                            surface_b_construction, "construction", "c_factor"
                        ),
                        "proposed_surface_c_factor": getattr_(
                            surface_p_construction, "construction", "c_factor"
                        ),
                    }
                else:
                    # Will never reach this line
                    # The OST defaults all unidentifiable surfaces to above wall grade
                    # Serve code completeness
                    raise Exception(f"Unrecognized surface type: {surface_b_type}")

            def rule_check(self, context, calc_vals, data=None):
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
