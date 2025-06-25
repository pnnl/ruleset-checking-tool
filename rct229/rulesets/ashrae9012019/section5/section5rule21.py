from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

FAIL_MSG = "Subsurface that is not regulated (Not part of building envelope) is not modeled with the same area, U-factor and SHGC in the baseline as in the propsoed design."


class PRM9012019Rule44m70(RuleDefinitionListIndexedBase):
    """Rule 21 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule44m70, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather", "constructions"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule44m70.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-21",
            description="Subsurface that is not regulated (not part of building envelope) must be modeled with the same area, U-factor and SHGC in the baseline as in the proposed design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(a) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_b["ruleset_model_descriptions"][0]["constructions"]
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule44m70.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule44m70.BuildingRule.UnregulatedSurfaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.BASELINE_0
            return {
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building, data["constructions"]
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0

            return (
                data["scc_dict_b"][surface_b["id"]] == SCC.UNREGULATED
                and len(surface_b.get("subsurfaces", [])) > 0
            )

        class UnregulatedSurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule44m70.BuildingRule.UnregulatedSurfaceRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    list_path="subsurfaces[*]",
                    each_rule=PRM9012019Rule44m70.BuildingRule.UnregulatedSurfaceRule.UnregulatedSubsurfaceRule(),
                    index_rmd=BASELINE_0,
                )

            class UnregulatedSubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        PRM9012019Rule44m70.BuildingRule.UnregulatedSurfaceRule.UnregulatedSubsurfaceRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        precision={
                            "subsurface_u_factor_b": {
                                "precision": 0.01,
                                "unit": "Btu/(hr*ft2*R)",
                            },
                            "subsurface_shgc_b": {
                                "precision": 0.01,
                                "unit": "",
                            },
                            "subsurface_glazed_area_b": {
                                "precision": 1,
                                "unit": "ft2",
                            },
                            "subsurface_opaque_area_b": {
                                "precision": 1,
                                "unit": "ft2",
                            },
                        },
                        fail_msg=FAIL_MSG,
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.BASELINE_0
                    subsurface_p = context.PROPOSED

                    return {
                        "subsurface_u_factor_b": CalcQ(
                            "thermal_transmittance", subsurface_b.get("u_factor")
                        ),
                        "subsurface_u_factor_p": CalcQ(
                            "thermal_transmittance", subsurface_p.get("u_factor")
                        ),
                        "subsurface_shgc_b": subsurface_b.get(
                            "solar_heat_gain_coefficient"
                        ),
                        "subsurface_shgc_p": subsurface_p.get(
                            "solar_heat_gain_coefficient"
                        ),
                        "subsurface_glazed_area_b": CalcQ(
                            "area", subsurface_b.get("glazed_area")
                        ),
                        "subsurface_glazed_area_p": CalcQ(
                            "area", subsurface_p.get("glazed_area")
                        ),
                        "subsurface_opaque_area_b": CalcQ(
                            "area", subsurface_b.get("opaque_area")
                        ),
                        "subsurface_opaque_area_p": CalcQ(
                            "area", subsurface_p.get("opaque_area")
                        ),
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    return (
                        self.precision_comparison["subsurface_u_factor_b"](
                            calc_vals["subsurface_u_factor_b"],
                            calc_vals["subsurface_u_factor_p"],
                        )
                        and self.precision_comparison["subsurface_shgc_b"](
                            calc_vals["subsurface_shgc_b"],
                            calc_vals["subsurface_shgc_p"],
                        )
                        and self.precision_comparison["subsurface_glazed_area_b"](
                            calc_vals["subsurface_glazed_area_b"],
                            calc_vals["subsurface_glazed_area_p"],
                        )
                        and self.precision_comparison["subsurface_opaque_area_b"](
                            calc_vals["subsurface_opaque_area_b"],
                            calc_vals["subsurface_opaque_area_p"],
                        )
                    )

                def is_tolerance_fail(self, context, calc_vals=None, data=None):
                    return (
                        std_equal(
                            calc_vals["subsurface_u_factor_b"],
                            calc_vals["subsurface_u_factor_p"],
                        )
                        and std_equal(
                            calc_vals["subsurface_shgc_b"],
                            calc_vals["subsurface_shgc_p"],
                        )
                        and std_equal(
                            calc_vals["subsurface_glazed_area_b"],
                            calc_vals["subsurface_glazed_area_p"],
                        )
                        and std_equal(
                            calc_vals["subsurface_opaque_area_b"],
                            calc_vals["subsurface_opaque_area_p"],
                        )
                    )
