from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_building_segment_skylight_roof_areas_dict import (
    get_building_segment_skylight_roof_areas_dict,
)
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal


class Section5Rule36(RuleDefinitionListIndexedBase):
    """Rule 36 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule36, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule36.BuildingRule(),
            index_rmr="baseline",
            id="5-36",
            description="Skylight area must be allocated to surfaces in the same proportion in the baseline as in the proposed design.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule36.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section5Rule36.BuildingRule.BuildingSegmentRule(),
                index_rmr="baseline",
                list_path="building_segments[*]",
            )

        def create_data(self, context, data=None):
            baseline = context.baseline
            proposed = context.proposed
            # Merge into the existing data dict
            return {
                **data,
                "scc_dictionary_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], baseline
                ),
                "skylight_roof_areas_dictionary_b": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], baseline
                ),
                "skylight_roof_areas_dictionary_p": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], proposed
                ),
            }

        class BuildingSegmentRule(RuleDefinitionListIndexedBase):
            def __ceil__(self):
                super(Section5Rule36.BuildingRule.BuildingSegmentRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    each_rule=Section5Rule36.BuildingRule.BuildingSegmentRule.SurfaceRule(),
                    index_rmr="baseline",
                )

            def create_data(self, context, data=None):
                building_segment_b = context.baseline
                building_segment_p = context.proposed

                return {
                    "scc_dictionary_b": data["scc_dictionary_b"],
                    "total_skylight_area_b": data["skylight_roof_areas_dictionary_b"][
                        building_segment_b["id"]
                    ]["total_skylight_area"],
                    "total_skylight_area_p": data["skylight_roof_areas_dictionary_p"][
                        building_segment_p["id"]
                    ]["total_skylight_area"],
                }

            def create_context_list(self, context, data=None):
                # create a list of regulated roof surfaces in baseline and proposed case
                scc = data["scc_dictionary_b"]

                surfaces_b = find_all("$..surfaces[*]", context.baseline)
                surfaces_p = find_all("$..surfaces[*]", context.proposed)

                # This assumes that the surfaces matched by IDs between proposed and baseline
                matched_proposed_surfaces = match_lists_by_id(surfaces_b, surfaces_p)

                proposed_baseline_surface_pairs = zip(
                    surfaces_b, matched_proposed_surfaces
                )

                return [
                    UserBaselineProposedVals(None, surface_b, surface_p)
                    for surface_b, surface_p in proposed_baseline_surface_pairs
                    if get_opaque_surface_type(surface_b) == OST.ROOF
                    and scc[surface_b["id"]] != SCC.UNREGULATED
                ]

            class SurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule36.BuildingRule.BuildingSegmentRule.SurfaceRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                    )

                def get_calc_vals(self, context, data=None):
                    total_skylight_area_b = data["total_skylight_area_b"]
                    total_skylight_area_p = data["total_skylight_area_p"]

                    roof_b = context.baseline
                    roof_p = context.proposed

                    total_skylight_area_surface_b = sum(
                        [
                            subsurface.get("glazed_area", ZERO.AREA)
                            + subsurface.get("opaque_area", ZERO.AREA)
                            for subsurface in find_all("subsurfaces[*]", roof_b)
                        ],
                        ZERO.AREA,
                    )
                    total_skylight_area_surface_p = sum(
                        [
                            subsurface.get("glazed_area", ZERO.AREA)
                            + subsurface.get("opaque_area", ZERO.AREA)
                            for subsurface in find_all("subsurfaces[*]", roof_p)
                        ],
                        ZERO.AREA,
                    )

                    return {
                        "skylight_surface_to_total_area_ratio_b": total_skylight_area_surface_b
                        / total_skylight_area_b,
                        "skylight_surface_to_total_area_ratio_p": total_skylight_area_surface_p
                        / total_skylight_area_p,
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    skylight_surface_total_area_ratio_b = calc_vals[
                        "skylight_surface_to_total_area_ratio_b"
                    ]
                    skylight_surface_total_area_ratio_p = calc_vals[
                        "skylight_surface_to_total_area_ratio_p"
                    ]
                    return std_equal(
                        skylight_surface_total_area_ratio_b,
                        skylight_surface_total_area_ratio_p,
                    )
