from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

FAIL_MSG = "Subsurface that is not regulated (Not part of building envelope) is not modeled with the same area, U-factor and SHGC in the baseline as in the propsoed design."


class Section5Rule28(RuleDefinitionListIndexedBase):
    """Rule 28 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule28, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule28.BuildingRule(),
            index_rmr="baseline",
            id="5-28",
            description="Subsurface that is not regulated (not part of building envelope) must be modeled with the same area, U-factor and SHGC in the baseline as in the proposed design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(a) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule28.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section5Rule28.BuildingRule.UnregulatedSurfaceRule(),
                index_rmr="baseline",
                list_path="$..surfaces[*]",
            )

        def create_data(self, context, data=None):
            building = context.baseline
            return {
                "scc_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.baseline

            return data["scc_dict_b"][surface_b["id"]] == SCC.UNREGULATED

        class UnregulatedSurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    Section5Rule28.BuildingRule.UnregulatedSurfaceRule, self
                ).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    list_path="subsurfaces[*]",
                    each_rule=Section5Rule28.BuildingRule.UnregulatedSurfaceRule.UnregulatedSubsurfaceRule(),
                    index_rmr="baseline",
                )

            class UnregulatedSubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule28.BuildingRule.UnregulatedSurfaceRule.UnregulatedSubsurfaceRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True),
                        fail_msg=FAIL_MSG,
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.baseline
                    subsurface_p = context.proposed

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
