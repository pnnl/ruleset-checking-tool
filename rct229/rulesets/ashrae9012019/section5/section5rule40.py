from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import \
    get_surface_conditioning_category_dict
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.schema.schema_enums import SchemaEnums

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
SUBSURFACE_SUBCLASSIFICATION_OPTIONS = SchemaEnums.schema_enums[
    "SubsurfaceSubclassificationOptions2019ASHRAE901"
]

MANUAL_CHECK_MSG = (
    "Zone has both residential and non-residential type spaces and the requirement for U-factor for "
    "doors are different. Verify door U-factor is modeled correctly. "
)
FAIL_MSG = ("Rule evaluation fails with a conservative outcome.")


class Section5Rule40(RuleDefinitionListIndexedBase):
    """Rule 33 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule40, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section5Rule40.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-40",
            description="U-factor of the baseline door is based on Tables G3.4-1 through G3.4-8 for the applicable door "
                        "type (swinging or non-swinging) and envelope conditioning category.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule40.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section5Rule40.BuildingRule.SurfaceRule(),
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
            return data["scc_dict_b"][surface_b["id"]] != SCC.UNREGULATED

        class SurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule40.BuildingRule.SurfaceRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    list_path="$.subsurfaces[*]",
                    required_fields={
                        "$.subsurfaces[*]": [
                            "classification",
                            "glazed_area",
                            "opaque_area", ],
                    },
                )

            def create_data(self, context, data):
                surface_b = context.BASELINE_0
                return {
                    "surface_conditioning_category_b": data[
                        "surface_conditioning_category_dict_b"
                    ][surface_b["id"]]
                }

            def list_filter(self, context_item, data):
                subsurface_b = context_item.BASELINE_0
                return (
                        subsurface_b["classification"] == DOOR
                        and subsurface_b["glazed_area"] <= subsurface_b["opaque_area"]
                )

            class SubSurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule40.BuildingRule.SurfaceRule.SubSurfaceRule, self
                    ).__init__(
                        rmrs_used=produce_ruleset_model_instance(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        required_fields={
                            "$": ["subclassification", "u_factor"],
                        },
                        manual_check_required_msg=MANUAL_CHECK_MSG,
                    )

                def is_applicable(self, context, data=None):
                    subsurface_b = context.BASELINE_0
                    surface_conditioning_category_b = data[
                        "surface_conditioning_category_b"
                    ]
                    climate_zone = data["climate_zone"]
                    target_u_factor_nonres = table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        DOOR,
                        subsurface_b["subclassification"],
                    )

                    target_u_factor_res = table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        DOOR,
                        subsurface_b["subclassification"],
                    )

                    return (
                            surface_conditioning_category_b == SCC.EXTERIOR_MIXED
                            and target_u_factor_nonres != target_u_factor_res
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.BASELINE_0
                    surface_conditioning_category_b = data[
                        "surface_conditioning_category_b"
                    ]
                    climate_zone = data["climate_zone"]

                    u_factor_b = subsurface_b["u_factor"]

                    target_u_factor_nonres = table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        DOOR,
                        subsurface_b["subclassification"],
                    )

                    target_u_factor_res = table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        DOOR,
                        subsurface_b["subclassification"],
                    )

                    target_u_factor_semiheated = table_G34_lookup(
                        climate_zone,
                        SCC.SEMI_EXTERIOR,
                        DOOR,
                        subsurface_b["subclassification"],
                    )
                    if surface_conditioning_category_b == SCC.EXTERIOR_NON_RESIDENTIAL:
                        target_u_factor = target_u_factor_nonres
                    elif surface_conditioning_category_b == SCC.EXTERIOR_RESIDENTIAL:
                        target_u_factor = target_u_factor_res
                    elif surface_conditioning_category_b == SCC.SEMI_EXTERIOR:
                        target_u_factor = target_u_factor_semiheated
                    else:
                        assert surface_conditioning_category_b == SCC.EXTERIOR_MIXED, (
                            f"Surface conditioning category is not one of the five types: EXTERIOR_NON_RESIDENTIAL, "
                            f"EXTERIOR_RESIDENTIAL, SEMI_EXTERIOR, EXTERIOR_MIXED, UNREGULATED, "
                            f"got {surface_conditioning_category_b} instead "
                        )
                        target_u_factor = target_u_factor_res

                    return {
                        "surface_conditioning_category_b": surface_conditioning_category_b,
                        "target_u_factor_res_b": target_u_factor_res["u_value"],
                        "target_u_factor_nonres_b": target_u_factor_nonres["u_value"],
                        "target_u_factor_semiheated_b": target_u_factor_semiheated[
                            "u_value"
                        ],
                        "u_factor_b": u_factor_b,
                        "target_u_factor_b": target_u_factor,
                    }

                def manual_check_required(self, context, calc_vals=None, data=None):
                    surface_conditioning_category_b = calc_vals[
                        "surface_conditioning_category_b"
                    ]
                    target_u_factor_res = calc_vals["target_u_factor_res_b"]
                    target_u_factor_nonres = calc_vals["target_u_factor_nonres_b"]
                    return (
                            surface_conditioning_category_b == SCC.EXTERIOR_MIXED
                            and target_u_factor_nonres != target_u_factor_res
                    )

                def get_manual_check_required_msg(
                        self, context, calc_vals=None, data=None
                ):
                    subsurface_b = context.BASELINE_0
                    return subsurface_b["subclassification"] in [
                        SUBSURFACE_SUBCLASSIFICATION_OPTIONS.SPANDREL_GLASS,
                        SUBSURFACE_SUBCLASSIFICATION_OPTIONS.GLASS_BLOCK,
                        SUBSURFACE_SUBCLASSIFICATION_OPTIONS.OTHER,
                    ]

                def rule_check(self, context, calc_vals=None, data=None):
                    u_factor_b = calc_vals["u_factor_b"]
                    target_u_factor_b = calc_vals["target_u_factor_b"]
                    return u_factor_b == target_u_factor_b

                def get_fail_msg(self, context, calc_vals=None, data=None):
                    u_factor_b = calc_vals["u_factor_b"]
                    target_u_factor_b = calc_vals["target_u_factor_b"]
                    if (u_factor_b < target_u_factor_b):
                        fail_msg = FAIL_MSG
                    else:
                        fail_msg = ""
                    return fail_msg
