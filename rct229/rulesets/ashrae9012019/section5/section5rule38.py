from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_scc_skylight_roof_ratios_dict import (
    get_building_scc_skylight_roof_ratios_dict,
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
from rct229.utils.std_comparisons import std_equal

MANUAL_CHECK_MSG = "MANUAL REVIEW IS REQUESTED TO VERIFY SKYLIGHT MEETS SHGC REQUIREMENT AS PER TABLE G3.4."


SURFACE_CLASSIFICATION = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"]


class Section5Rule38(RuleDefinitionListIndexedBase):
    """Rule 38 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule38, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section5Rule38.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-38",
            description="Skylight SHGC properties shall match the appropriate requirements in Tables G3.4-1 through G3.4-8 using the value and the applicable skylight percentage.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule38.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                list_path="$.building_segments[*].zones[*].surfaces[*]",
                each_rule=Section5Rule38.BuildingRule.RoofRule(),
                index_rmr=BASELINE_0,
                manual_check_required_msg=MANUAL_CHECK_MSG,
            )

        def manual_check_required(self, context, calc_vals=None, data=None):
            building_b = context.BASELINE_0
            climate_zone = data["climate_zone"]

            building_scc_skylight_roof_ratios_dict_b = (
                get_building_scc_skylight_roof_ratios_dict(climate_zone, building_b)
            )

            target_shgc_2per_residential = table_G34_lookup(
                climate_zone,
                "EXTERIOR RESIDENTIAL",
                "SKYLIGHT",
                skylit_wwr=0.0,
            )["solar_heat_gain_coefficient"]

            target_shgc_above2_residential = table_G34_lookup(
                climate_zone,
                "EXTERIOR RESIDENTIAL",
                "SKYLIGHT",
                skylit_wwr=0.021,
            )["solar_heat_gain_coefficient"]

            target_shgc_2per_nonresidential = table_G34_lookup(
                climate_zone,
                "EXTERIOR NON-RESIDENTIAL",
                "SKYLIGHT",
                skylit_wwr=0.021,
            )["solar_heat_gain_coefficient"]

            target_shgc_above2_nonresidential = table_G34_lookup(
                climate_zone,
                "EXTERIOR NON-RESIDENTIAL",
                "SKYLIGHT",
                skylit_wwr=0.021,
            )["solar_heat_gain_coefficient"]

            return all(
                [
                    building_scc_skylight_roof_ratios_dict_b[SCC.EXTERIOR_MIXED] > 0,
                    target_shgc_2per_residential == target_shgc_above2_residential,
                    target_shgc_2per_nonresidential
                    == target_shgc_above2_nonresidential,
                    target_shgc_2per_residential == target_shgc_2per_nonresidential,
                ]
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            climate_zone = data["climate_zone"]
            scc_skylight_roof_ratios_dict_b = (
                get_building_scc_skylight_roof_ratios_dict(climate_zone, building_b)
            )

            if scc_skylight_roof_ratios_dict_b[SCC.EXTERIOR_RESIDENTIAL] > 0.02:
                target_shgc_res = table_G34_lookup(
                    climate_zone,
                    "EXTERIOR RESIDENTIAL",
                    "SKYLIGHT",
                    skylit_wwr=0.021,
                )["solar_heat_gain_coefficient"]
            else:
                target_shgc_res = table_G34_lookup(
                    climate_zone,
                    "EXTERIOR RESIDENTIAL",
                    "SKYLIGHT",
                    skylit_wwr=0.0,
                )["solar_heat_gain_coefficient"]

            if scc_skylight_roof_ratios_dict_b[SCC.EXTERIOR_NON_RESIDENTIAL] > 0.02:
                target_shgc_nonres = table_G34_lookup(
                    climate_zone,
                    "EXTERIOR NON-RESIDENTIAL",
                    "SKYLIGHT",
                    skylit_wwr=0.021,
                )["solar_heat_gain_coefficient"]
            else:
                target_shgc_nonres = table_G34_lookup(
                    climate_zone,
                    "EXTERIOR NON-RESIDENTIAL",
                    "SKYLIGHT",
                    skylit_wwr=0,
                )["solar_heat_gain_coefficient"]

            if scc_skylight_roof_ratios_dict_b[SCC.SEMI_EXTERIOR]:
                target_shgc_semiheated = table_G34_lookup(
                    climate_zone,
                    "SEMI-EXTERIOR",
                    "SKYLIGHT",
                    skylit_wwr=0.021,
                )["solar_heat_gain_coefficient"]
            else:
                target_shgc_semiheated = table_G34_lookup(
                    climate_zone,
                    "SEMI-EXTERIOR",
                    "SKYLIGHT",
                    skylit_wwr=0,
                )["solar_heat_gain_coefficient"]

            return {
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    climate_zone, building_b
                ),
                "target_shgc_res": target_shgc_res,
                "target_shgc_nonres": target_shgc_nonres,
                "target_shgc_semiheated": target_shgc_semiheated,
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            scc = data["surface_conditioning_category_dict"][surface_b["id"]]

            return (
                get_opaque_surface_type(surface_b) == OST.ROOF
                and surface_b.get("subsurfaces")
                and scc != SCC.UNREGULATED
            )

        class RoofRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule38.BuildingRule.RoofRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    each_rule=Section5Rule38.BuildingRule.RoofRule.SubsurfaceRule(),
                    index_rmr=BASELINE_0,
                    list_path="subsurfaces[*]",
                    manual_check_required_msg=MANUAL_CHECK_MSG,
                )

            def create_data(self, context, data=None):
                surface_b = context.BASELINE_0
                surface_id_b = surface_b["id"]

                return {"surface_id_b": surface_id_b}

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule38.BuildingRule.RoofRule.SubsurfaceRule, self
                    ).__init__(
                        rmrs_used=produce_ruleset_model_instance(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                        required_fields={
                            "$": ["classification", "glazed_area", "opaque_area"]
                        },
                    )

                def is_applicable(self, context, data=None):
                    subsurface_b = context.BASELINE_0

                    return (
                        subsurface_b["classification"] == SURFACE_CLASSIFICATION.DOOR
                        and subsurface_b["glazed_area"] > subsurface_b["opaque_area"]
                    ) or subsurface_b["classification"] != SURFACE_CLASSIFICATION.DOOR

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.BASELINE_0
                    subsurface_shgc_b = subsurface_b["solar_heat_gain_coefficient"]

                    subsuface_type_b = data["surface_conditioning_category_dict"][
                        data["surface_id_b"]
                    ]
                    target_shgc_res_b = data["target_shgc_res"]
                    target_shgc_nonres_b = data["target_shgc_nonres"]
                    target_shgc_semiheated_b = data["target_shgc_semiheated"]
                    target_shgc = 0.0

                    if (
                        subsuface_type_b == SCC.EXTERIOR_MIXED
                        or subsuface_type_b == SCC.EXTERIOR_RESIDENTIAL
                    ):
                        target_shgc = target_shgc_res_b
                    elif subsuface_type_b == SCC.EXTERIOR_NON_RESIDENTIAL:
                        target_shgc = target_shgc_nonres_b
                    else:
                        target_shgc = target_shgc_semiheated_b

                    return {
                        "subsurface_shgc_b": subsurface_shgc_b,
                        "target_shgc": target_shgc,
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    target_shgc = calc_vals["target_shgc"]
                    subsurface_shgc_b = calc_vals["subsurface_shgc_b"]

                    return std_equal(target_shgc, subsurface_shgc_b)
