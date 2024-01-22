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
from rct229.utils.std_comparisons import std_equal

TARGET_ABSORPTANCE_SOLAR_EXTERIOR = 0.7


class Section5Rule31(RuleDefinitionListIndexedBase):
    """Rule 31 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule31, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule31.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-31",
            description=" The baseline roof surfaces shall be modeled using a solar reflectance of 0.30",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(g) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule31.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section5Rule31.BuildingRule.RoofRule(),
                index_rmr=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            return {
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            return (
                get_opaque_surface_type(surface_b) == OST.ROOF
                and data["scc_dict_b"][surface_b["id"]] != SCC.UNREGULATED
            )

        class RoofRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule31.BuildingRule.RoofRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["optical_properties"],
                        "optical_properties": ["absorptance_solar_exterior"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                roof_b = context.BASELINE_0
                return {
                    "absorptance_solar_exterior": roof_b["optical_properties"][
                        "absorptance_solar_exterior"
                    ]
                }

            def rule_check(self, context, calc_vals=None, data=None):
                return std_equal(
                    TARGET_ABSORPTANCE_SOLAR_EXTERIOR,
                    calc_vals["absorptance_solar_exterior"],
                )
