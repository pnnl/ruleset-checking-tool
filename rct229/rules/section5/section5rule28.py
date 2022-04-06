from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as OST,
)
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


class Section5Rule28(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule28, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule28.BuildingRule(),
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
            super(Section5Rule28.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section5Rule28.BuildingRule.UnregulatedSurfaceRule(),
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

        class UnregulatedSurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    Section5Rule28.BuildingRule.UnregulatedSurfaceRule, self
                ).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    list_path="subsurfaces[*]"
                )

            class UnregulatedSubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule28.BuildingRule.UnregulatedSurfaceRule.UnregulatedSubsurfaceRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True),
                        required_fields={
                            "$": [
                                "u_factor",
                                "solar_heat_gain_coefficient",
                                "glazed_area",
                                "opaque_area",
                            ]
                        },
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.baseline
                    subsurface_p = context.proposed

                    return {
                        "baseline_subsurface_u_factor": subsurface_b["u_factor"],
                        "proposed_subsurface_u_factor": subsurface_p["u_factor"],
                        "baseline_subsurface_shgc": subsurface_b[
                            "solar_heat_gain_coefficient"
                        ],
                        "proposed_subsurface_shgc": subsurface_p[
                            "solar_heat_gain_coefficient"
                        ],
                        "baseline_subsurface_glazed_area": subsurface_b["glazed_area"],
                        "proposed_subsurface_glazed_area": subsurface_p["glazed_area"],
                        "baseline_subsurface_opaque_area": subsurface_b["opaque_area"],
                        "proposed_subsurface_opaque_area": subsurface_p["opaque_area"],
                    }

                def rule_check(self, context, calc_vals, data=None):
                    return std_equal(
                            calc_vals["baseline_subsurface_u_factor"],
                            calc_vals["proposed_subsurface_u_factor"],
                        ) and std_equal(
                            calc_vals["solar_heat_gain_coefficient"],
                            calc_vals["solar_heat_gain_coefficient"],
                        ) and std_equal(
                            calc_vals["glazed_area"], calc_vals["glazed_area"]
                        ) and std_equal(
                            calc_vals["opaque_area"], calc_vals["opaque_area"]
                        )
