from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_building_scc_skylight_roof_ratios_dict import (
    get_building_scc_skylight_roof_ratios_dict,
)
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.std_comparisons import std_equal

MANUAL_CHECK_MSG = "Manual review is required to verify skylight meets U-factor requirement as per table G3.4."


SURFACE_CLASSIFICATION = schema_enums["SubsurfaceClassificationOptions"]


class Section5Rule38(RuleDefinitionListIndexedBase):
    """Rule 38 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule38, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule38.BuildingRule(),
            index_rmr="baseline",
            id="5-38",
            description="Skylight SHGC properties shall match the appropriate requirements in Tables G3.4-1 through G3.4-8 using the value and the applicable skylight percentage.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule38.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                list_path="$..surfaces[*]",
                each_rule=Section5Rule38.BuildingRule.SurfaceRule(),
                index_rmr="baseline",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            climate_zone = data["climate_zone"]

            scc_skylight_roof_ratios_dict_b = (
                get_building_scc_skylight_roof_ratios_dict(climate_zone, building_b)
            )

            manual_review_flag = False
            target_shgc_mixed = None
            target_shgc_res = None
            target_shgc_nonres = None
            target_shgc_semiheated = None
            if scc_skylight_roof_ratios_dict_b["EXTERIOR MIXED"] > 0:
                if (
                    table_G34_lookup(
                        climate_zone,
                        "EXTERIOR RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0.0,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        "EXTERIOR RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0.021,
                    )["solar_heat_gain_coefficient"]
                    and table_G34_lookup(
                        climate_zone,
                        "EXTERIOR NON-RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0.021,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        "EXTERIOR NON-RESIDENTIAL" "SKYLIGHT",
                        skylit_wwr=0.021,
                    )["solar_heat_gain_coefficient"]
                    and table_G34_lookup(
                        climate_zone,
                        "EXTERIOR RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        "EXTERIOR NON-RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0.021,
                    )["solar_heat_gain_coefficient"]
                    and table_G34_lookup(
                        climate_zone,
                        "EXTERIOR RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        "EXTERIOR NON-RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0,
                    )["solar_heat_gain_coefficient"]
                ):
                    target_shgc_mixed = table_G34_lookup(
                        climate_zone,
                        "EXTERIOR RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0.0,
                    )["solar_heat_gain_coefficient"]
                else:
                    manual_review_flag = True
            else:
                if scc_skylight_roof_ratios_dict_b[SCC.EXTERIOR_RESIDENTIAL] > 0.02:
                    target_shgc_res = table_G34_lookup(
                        climate_zone,
                        "SEMIHEATED",
                        "SKYLIGHT",
                        skylit_wwr=0.021,
                    )["solar_heat_gain_coefficient"]
                else:
                    target_shgc_res = table_G34_lookup(
                        climate_zone,
                        "SEMIHEATED",
                        skylit_wwr=0.021,
                    )["solar_heat_gain_coefficient"]

                if scc_skylight_roof_ratios_dict_b["NON-RESIDENTIAL"] > 0.02:
                    target_shgc_nonres = table_G34_lookup(
                        climate_zone,
                        "NON-RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0.021,
                    )["solar_heat_gain_coefficient"]
                else:
                    target_shgc_nonres = table_G34_lookup(
                        climate_zone,
                        "NON-RESIDENTIAL",
                        "SKYLIGHT",
                        skylit_wwr=0,
                    )["solar_heat_gain_coefficient"]

                if scc_skylight_roof_ratios_dict_b["SEMI-EXTERIOR"]:
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
                "target_shgc_mixed": target_shgc_mixed,
                "target_shgc_res": target_shgc_res,
                "target_shgc_nonres": target_shgc_nonres,
                "target_shgc_semiheated": target_shgc_semiheated,
                "manual_review_flag": manual_review_flag,
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.baseline
            scc = data["surface_conditioning_category_dict"][surface_b["id"]]

            return (
                get_opaque_surface_type(surface_b) == OST.ROOF
                and surface_b.get("subsurfaces")
                and scc is not SCC.UNREGULATED
            )

        class SurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule38.BuildingRule.SurfaceRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    each_rule=Section5Rule38.BuildingRule.SurfaceRule.SubsurfaceRule(),
                    index_rmr="baseline",
                    list_path="subsurfaces[*]",
                    manual_check_required_msg=MANUAL_CHECK_MSG,
                )

            def create_data(self, context, data=None):
                surface_b = context.baseline
                surface_id_b = surface_b["id"]
                return {"surface_id_b": surface_id_b}

            def list_filter(self, context_item, data=None):
                subsurface_b = context_item.baseline

                return (
                    subsurface_b.get("classification") == SURFACE_CLASSIFICATION.DOOR
                    and subsurface_b.get("glazed_area")
                    > subsurface_b.get("opaque_area")
                ) or subsurface_b.get("classification") != SURFACE_CLASSIFICATION.DOOR

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule38.BuildingRule.SurfaceRule.SubsurfaceRule, self
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                        # required_fields={"$": ["has_manual_interior_shades"]}, # should be updated
                    )

                def manual_check_required(self, context, calc_vals=None, data=None):
                    manual_review_flag = data["manual_review_flag"]
                    subsurface_scc_b = data["surface_conditioning_category_dict"][
                        data["surface_id_b"]
                    ]

                    return (
                        manual_review_flag
                        # and subsurface_scc_b == SCC.EXTERIOR_MIXED
                    )

                def rule_check(self, context, calc_vals=None, data=None):
                    subsurface_b = context.baseline
                    subsuface_type_b = data["surface_conditioning_category_dict"][
                        data["surface_id_b"]
                    ]
                    target_shgc_mixed = data["target_shgc_mixed"]
                    target_shgc_res = data["target_shgc_res"]
                    target_shgc_nonres = data["target_shgc_nonres"]
                    target_shgc_semiheated = data["target_shgc_semiheated"]

                    return (
                        (
                            subsuface_type_b == SCC.EXTERIOR_MIXED
                            and target_shgc_mixed is not None
                            and std_equal(
                                subsurface_b["solar_heat_gain_coefficient"],
                                target_shgc_mixed,
                            )
                        )
                        or (
                            subsuface_type_b == SCC.EXTERIOR_RESIDENTIAL
                            and target_shgc_res is not None
                            and std_equal(
                                subsurface_b["solar_heat_gain_coefficient"],
                                target_shgc_res,
                            )
                        )
                        or (
                            subsuface_type_b == SCC.EXTERIOR_NON_RESIDENTIAL
                            and target_shgc_nonres is not None
                            and std_equal(
                                subsurface_b["solar_heat_gain_coefficient"],
                                target_shgc_nonres,
                            )
                        )
                        or (
                            subsuface_type_b == SCC.SEMI_EXTERIOR
                            and target_shgc_semiheated is not None
                            and std_equal(
                                subsurface_b["solar_heat_gain_coefficient"],
                                target_shgc_semiheated,
                            )
                        )
                    )
