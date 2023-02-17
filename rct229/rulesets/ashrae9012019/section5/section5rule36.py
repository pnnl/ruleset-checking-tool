from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_skylight_roof_areas_dict import (
    get_building_segment_skylight_roof_areas_dict,
)
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
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
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
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule36.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section5Rule36.BuildingRule.BuildingSegmentRule(),
                index_rmr="baseline",
                list_path="building_segments[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            building_p = context.proposed
            return {
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
                "skylight_roof_areas_dictionary_b": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], building_b
                ),
                "skylight_roof_areas_dictionary_p": get_building_segment_skylight_roof_areas_dict(
                    data["climate_zone"], building_p
                ),
            }

        class BuildingSegmentRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule36.BuildingRule.BuildingSegmentRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    each_rule=Section5Rule36.BuildingRule.BuildingSegmentRule.RoofRule(),
                    index_rmr="baseline",
                    list_path="$..surfaces[*]",
                )

            def create_data(self, context, data=None):
                building_segment_b = context.baseline
                building_segment_p = context.proposed
                return {
                    "scc_dict_b": data["scc_dict_b"],
                    "total_skylight_area_b": data["skylight_roof_areas_dictionary_b"][
                        building_segment_b["id"]
                    ]["total_skylight_area"],
                    "total_skylight_area_p": data["skylight_roof_areas_dictionary_p"][
                        building_segment_p["id"]
                    ]["total_skylight_area"],
                }

            def list_filter(self, context_item, data=None):
                scc = data["scc_dict_b"]
                surface_b = context_item.baseline
                return (
                    get_opaque_surface_type(surface_b) == OST.ROOF
                    and scc[surface_b["id"]] != SCC.UNREGULATED
                )

            class RoofRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule36.BuildingRule.BuildingSegmentRule.RoofRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True),
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
                        "total_skylight_area_b": CalcQ("area", total_skylight_area_b),
                        "total_skylight_area_p": CalcQ("area", total_skylight_area_p),
                        "total_skylight_area_surface_b": CalcQ(
                            "area", total_skylight_area_surface_b
                        ),
                        "total_skylight_area_surface_p": CalcQ(
                            "area", total_skylight_area_surface_p
                        ),
                    }

                def rule_check(self, context, calc_vals=None, data=None):

                    total_skylight_area_b = calc_vals["total_skylight_area_b"]
                    total_skylight_area_p = calc_vals["total_skylight_area_p"]
                    total_skylight_area_surface_b = calc_vals[
                        "total_skylight_area_surface_b"
                    ]
                    total_skylight_area_surface_p = calc_vals[
                        "total_skylight_area_surface_p"
                    ]

                    return (
                        # both segments have no skylight area
                        total_skylight_area_b == 0
                        and total_skylight_area_p == 0
                        and total_skylight_area_surface_b == 0
                        and total_skylight_area_surface_p == 0
                    ) or (
                        # product to ensure neither is 0 & short-circuit logic if either of them is 0.
                        total_skylight_area_b * total_skylight_area_p > 0
                        # both segments' skylight area ratios are the same
                        and std_equal(
                            total_skylight_area_surface_b / total_skylight_area_b,
                            total_skylight_area_surface_p / total_skylight_area_p,
                        )
                    )
