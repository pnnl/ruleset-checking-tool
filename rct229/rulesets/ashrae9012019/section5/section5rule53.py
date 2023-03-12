from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)

DOOR = schema_enums["SubsurfaceClassificationOptions"].DOOR
METAL_COILING_DOOR = schema_enums[
    "SubsurfaceSubclassificationOptions2019ASHRAE901"
].METAL_COILING_DOOR
NONSWINGING_DOOR = schema_enums[
    "SubsurfaceSubclassificationOptions2019ASHRAE901"
].NONSWINGING_DOOR
SECTIONAL_GARAGE_DOOR = schema_enums[
    "SubsurfaceSubclassificationOptions2019ASHRAE901"
].SECTIONAL_GARAGE_DOOR
SWINGING_DOOR = schema_enums[
    "SubsurfaceSubclassificationOptions2019ASHRAE901"
].SWINGING_DOOR

MANUAL_CHECK_MSG = (
    "Zone has both residential and non-residential type spaces and the requirement for U-factor for "
    "doors are different. Verify door U-factor is modeled correctly. "
)


class Section5Rule53(RuleDefinitionListIndexedBase):
    """Rule 53 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule53, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule53.BuildingRule(),
            index_rmr="baseline",
            id="5-53",
            description="U-factor of the baseline door is based on Tables G3.4-1 through G3.4-8 for the applicable "
            "door type (swinging or non-swinging) and envelope conditioning category.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline model.",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule53.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule53.BuildingRule.SurfaceRule(),
                index_rmr="baseline",
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def is_applicable(self, context, data=None):
            # It is unclear which level the rule checks for applicability.
            # This implementation follows the Applicability Check in the RDS
            building_p = context.baseline
            subsurfaces = find_all(
                "$.building_segments[*].zones[*].surfaces[*].subsurfaces[*]", building_p
            )
            return any(
                [
                    subsurface_b.get("classification") == DOOR
                    and subsurface_b.get("glazed_area", ZERO.AREA)
                    >= subsurface_b.get("opaque_area", ZERO.AREA)
                    for subsurface_b in subsurfaces
                ]
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            climate_zone = data["climate_zone"]
            return {
                "surface_conditioning_category_dict_b": get_surface_conditioning_category_dict(
                    climate_zone, building_b
                )
            }

        def list_filter(self, context_item, data=None):
            # context_item shall be the list of the list_path element
            surface_b = context_item.baseline
            # exclude unregulated surfaces
            return (
                data["surface_conditioning_category_dict_b"][surface_b["id"]]
                != SCC.UNREGULATED
            )

        class SurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule53.BuildingRule.SurfaceRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    each_rule=Section5Rule53.BuildingRule.SurfaceRule.SubSurfaceRule(),
                    index_rmr="baseline",
                    list_path="$.subsurfaces[*]",
                    required_fields={
                        "$.subsurfaces[*]": [
                            "classification",
                            "glazed_area",
                            "opaque_area",
                        ]
                    },
                )

            def create_data(self, context, data):
                surface_b = context.baseline
                return {
                    "surface_conditioning_category_b": data[
                        "surface_conditioning_category_dict_b"
                    ][surface_b["id"]]
                }

            def list_filter(self, context_item, data):
                subsurface_b = context_item.baseline
                # exclude non door surfaces and doors whose opaque area is greater than glazed area
                return (
                    subsurface_b["classification"] == DOOR
                    and subsurface_b["glazed_area"] >= subsurface_b["opaque_area"]
                )

            class SubSurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule53.BuildingRule.SurfaceRule.SubSurfaceRule, self
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                        required_fields={
                            "$": ["subclassification", "u_factor"],
                        },
                        manual_check_required_msg=MANUAL_CHECK_MSG,
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.baseline
                    surface_conditioning_category_b = data[
                        "surface_conditioning_category_b"
                    ]
                    climate_zone = data["climate_zone"]

                    u_factor_b = subsurface_b["u_factor"]

                    target_u_factor_nonres = table_G34_lookup(
                        climate_zone,
                        surface_conditioning_category_b,
                        DOOR,
                        subsurface_b["subclassification"],
                    )

                    target_u_factor_res = table_G34_lookup(
                        climate_zone,
                        surface_conditioning_category_b,
                        DOOR,
                        subsurface_b["subclassification"],
                    )

                    target_u_factor_semiheated = table_G34_lookup(
                        climate_zone,
                        surface_conditioning_category_b,
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
                        # This step should only be exterior mixed surface conditioning type
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

                def rule_check(self, context, calc_vals=None, data=None):
                    u_factor_b = calc_vals["u_factor_b"]
                    target_u_factor_b = calc_vals["target_u_factor_b"]
                    return u_factor_b == target_u_factor_b
