from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.std_comparisons import std_equal

TARGET_ABSORPTANCE_SOLAR_EXTERIOR = 0.7


class Section5Rule42(RuleDefinitionListIndexedBase):
    """Rule 42 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule42, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule42.BuildingRule(),
            index_rmr="baseline",
            id="5-42",
            description=" The baseline roof surfaces shall be modeled using a solar reflectance of 0.30",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(g) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule42.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule42.BuildingRule.RoofRule(),
                index_rmr="baseline",
                list_path="$..surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            return {
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.baseline
            return (
                get_opaque_surface_type(surface_b) == OST.ROOF
                and data["scc_dict_b"][surface_b["id"]] != SCC.UNREGULATED
            )

        class RoofRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule42.BuildingRule.RoofRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    required_fields={
                        "$": ["surface_optical_properties"],
                        "surface_optical_properties": ["absorptance_solar_exterior"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                roof_b = context.baseline
                return {
                    "absorptance_solar_exterior": roof_b["surface_optical_properties"][
                        "absorptance_solar_exterior"
                    ]
                }

            def rule_check(self, context, calc_vals=None, data=None):
                return std_equal(
                    TARGET_ABSORPTANCE_SOLAR_EXTERIOR,
                    calc_vals["absorptance_solar_exterior"],
                )
