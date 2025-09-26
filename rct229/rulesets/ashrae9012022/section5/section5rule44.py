from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType,
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.utils.assertions import getattr_
from rct229.utils.std_comparisons import std_equal

REQ_ABS_SOLAR_EXT = 0.75


class PRM9012022Rule13d92(RuleDefinitionListIndexedBase):
    """Rule 44 of ASHRAE 90.1-2022 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012022Rule13d92, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012022Rule13d92.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-44",
            description="The baseline above-grade wall surfaces shall be modeled with a solar reflectance of 0.25.",
            ruleset_section_title="Envelope",
            standard_section="Table G3.1 Section 5(j) Baseline",
            is_primary_rule=True,
            list_path="$.ruleset_model_descriptions[*].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmd_b = context.BASELINE_0
        climate_zone_b = rmd_b["ruleset_model_descriptions"][0]["weather"][
            "climate_zone"
        ]
        constructions_b = rmd_b["ruleset_model_descriptions"][0].get("constructions")

        return {"climate_zone_b": climate_zone_b, "constructions_b": constructions_b}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012022Rule13d92.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012022Rule13d92.BuildingRule.SurfaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            climate_zone_b = data["climate_zone_b"]
            constructions_b = data["constructions_b"]

            scc_dict_b = get_surface_conditioning_category_dict(
                climate_zone_b, building_b, constructions_b
            )

            return {"scc_dict_b": scc_dict_b}

        class SurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012022Rule13d92.BuildingRule.SurfaceRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    precision={
                        "surface_optical_properties_b": {
                            "precision": 0.01,
                            "unit": "",
                        },
                    },
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.BASELINE_0
                scc_dict_b = data["scc_dict_b"]

                surface_optical_properties_b = 0.0
                if (
                    get_opaque_surface_type(surface_b)
                    == OpaqueSurfaceType.ABOVE_GRADE_WALL
                    and scc_dict_b[surface_b["id"]] != SCC.UNREGULATED
                ):
                    surface_optical_properties_b = getattr_(
                        surface_b, "surfaces", "surface_optical_properties"
                    )

                return {"surface_optical_properties_b": surface_optical_properties_b}

            def rule_check(self, context, calc_vals=None, data=None):
                surface_optical_properties_b = calc_vals["surface_optical_properties_b"]

                return self.precision_comparison["surface_optical_properties_b"](
                    surface_optical_properties_b, REQ_ABS_SOLAR_EXT
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                surface_optical_properties_b = calc_vals["surface_optical_properties_b"]

                return std_equal(surface_optical_properties_b, REQ_ABS_SOLAR_EXT)
