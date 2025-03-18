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
from rct229.utils.jsonpath_utils import find_one
from rct229.schema.schema_enums import SchemaEnums

EXTERIOR = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"].EXTERIOR


class Section5Rule40(RuleDefinitionListIndexedBase):
    """Rule 40 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule40, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section5Rule40.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-40",
            description="Opaque roof surfaces that are not regulated (not part of opaque building envelope) must be "
            "modeled with the same thermal emittance and solar reflectance in the baseline as in the "
            "proposed design. ",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        return {"climate_zone": climate_zone}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule40.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section5Rule40.BuildingRule.RoofRule(),
                index_rmd=BASELINE_0,
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
            scc = data["scc_dict_b"][surface_b["id"]]
            return (
                get_opaque_surface_type(surface_b) == OST.ROOF
                and surface_b.get("adjacent_to") == EXTERIOR
                and scc is SCC.UNREGULATED
            )

        class RoofRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule40.BuildingRule.RoofRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    precision={
                        "absorptance_thermal_exterior_b": {
                            "precision": 0.01,
                            "unit": "",
                        },
                        "absorptance_solar_exterior_b": {
                            "precision": 0.01,
                            "unit": "",
                        },
                    },
                )

            def get_calc_vals(self, context, data=None):
                roof_b = context.BASELINE_0
                roof_p = context.PROPOSED
                return {
                    "absorptance_solar_exterior_b": find_one(
                        "$.optical_properties.absorptance_solar_exterior", roof_b
                    ),
                    "absorptance_solar_exterior_p": find_one(
                        "$.optical_properties.absorptance_solar_exterior", roof_p
                    ),
                    "absorptance_thermal_exterior_b": find_one(
                        "$.optical_properties.absorptance_thermal_exterior", roof_b
                    ),
                    "absorptance_thermal_exterior_p": find_one(
                        "$.optical_properties.absorptance_thermal_exterior", roof_p
                    ),
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                absorptance_solar_exterior_b = calc_vals["absorptance_solar_exterior_b"]
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                absorptance_thermal_exterior_b = calc_vals[
                    "absorptance_thermal_exterior_b"
                ]
                absorptance_thermal_exterior_p = calc_vals[
                    "absorptance_thermal_exterior_p"
                ]
                return any(
                    absorptance_property == None
                    for absorptance_property in [
                        absorptance_solar_exterior_b,
                        absorptance_solar_exterior_p,
                        absorptance_thermal_exterior_b,
                        absorptance_thermal_exterior_p,
                    ]
                )

            def rule_check(self, context, calc_vals=None, data=None):
                absorptance_solar_exterior_b = calc_vals["absorptance_solar_exterior_b"]
                absorptance_solar_exterior_p = calc_vals["absorptance_solar_exterior_p"]
                absorptance_thermal_exterior_b = calc_vals[
                    "absorptance_thermal_exterior_b"
                ]
                absorptance_thermal_exterior_p = calc_vals[
                    "absorptance_thermal_exterior_p"
                ]
                return self.precision_comparison["absorptance_solar_exterior_b"](
                    absorptance_solar_exterior_b, absorptance_solar_exterior_p
                ) and self.precision_comparison["absorptance_thermal_exterior_b"](
                    absorptance_thermal_exterior_b, absorptance_thermal_exterior_p
                )
