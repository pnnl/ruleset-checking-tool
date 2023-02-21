from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_standard_val import std_le
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
from rct229.utils.pint_utils import ZERO, CalcQ

MANUAL_CHECK_MSG = "Manual review is required to verify skylight meets U-factor requirement as per table G3.4."
MANUAL_CHECK_APPLICABLE = (
    "The subsurface type is Door, not applicable for the rule-checking"
)
DOOR = schema_enums["SubsurfaceClassificationOptions"].DOOR


class Section5Rule37(RuleDefinitionListIndexedBase):
    """Rule 37 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule37, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule37.BuildingRule(),
            index_rmr="baseline",
            id="5-37",
            description="Skylight U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule37.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule37.BuildingRule.RoofRule(),
                index_rmr="baseline",
                list_path="$.building_segments[*].zones[*].surfaces[*]",
                manual_check_required_msg=MANUAL_CHECK_MSG,
            )

        def manual_check_required(self, context, calc_vals=None, data=None):
            # If building segment exterior mixed skylight to roof ratio is greater than 0
            # and residential, nonresidential and <=2% and > 2% u_factors are identical
            # then set the manual check required and stop execution.
            building_b = context.baseline
            climate_zone = data["climate_zone"]
            building_scc_skylight_roof_ratios_dict_b = (
                get_building_scc_skylight_roof_ratios_dict(climate_zone, building_b)
            )
            target_exterior_2per_residential = table_G34_lookup(
                climate_zone,
                SCC.EXTERIOR_RESIDENTIAL,
                "SKYLIGHT",
                skylit_wwr=0.02,
            )
            target_exterior_2per_nonresidential = table_G34_lookup(
                climate_zone,
                SCC.EXTERIOR_NON_RESIDENTIAL,
                "SKYLIGHT",
                skylit_wwr=0.02,
            )
            target_exterior_above2_residential = table_G34_lookup(
                climate_zone,
                SCC.EXTERIOR_RESIDENTIAL,
                "SKYLIGHT",
                skylit_wwr=0.03,
            )
            target_exterior_above2_nonresidential = table_G34_lookup(
                climate_zone,
                SCC.EXTERIOR_NON_RESIDENTIAL,
                "SKYLIGHT",
                skylit_wwr=0.03,
            )
            return building_scc_skylight_roof_ratios_dict_b[
                SCC.EXTERIOR_MIXED
            ] > 0 and (
                target_exterior_2per_residential["u_value"]
                != target_exterior_2per_nonresidential["u_value"]
                or target_exterior_above2_residential["u_value"]
                != target_exterior_above2_nonresidential["u_value"]
                or target_exterior_2per_residential["u_value"]
                != target_exterior_2per_nonresidential["u_value"]
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            climate_zone = data["climate_zone"]
            building_scc_skylight_roof_ratios_dict_b = (
                get_building_scc_skylight_roof_ratios_dict(climate_zone, building_b)
            )

            # Process target_u_factor_res
            srr_res = building_scc_skylight_roof_ratios_dict_b[SCC.EXTERIOR_RESIDENTIAL]
            target_u_factor_res = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_RESIDENTIAL,
                    "SKYLIGHT",
                    skylit_wwr=0.02,
                )
                if srr_res > 0.02
                else table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_RESIDENTIAL,
                    "SKYLIGHT",
                    skylit_wwr=0.03,
                )
            )
            # Process target_u_factor_nonres
            srr_nonres = building_scc_skylight_roof_ratios_dict_b[
                SCC.EXTERIOR_NON_RESIDENTIAL
            ]
            target_u_factor_nonres = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    "SKYLIGHT",
                    skylit_wwr=0.02,
                )
                if srr_nonres > 0.02
                else table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    "SKYLIGHT",
                    skylit_wwr=0.03,
                )
            )
            # Process target_u_factor_semiheated
            srr_semi_exterior = building_scc_skylight_roof_ratios_dict_b[
                SCC.SEMI_EXTERIOR
            ]
            target_u_factor_semiheated = (
                table_G34_lookup(
                    climate_zone,
                    SCC.SEMI_EXTERIOR,
                    "SKYLIGHT",
                    skylit_wwr=0.02,
                )
                if srr_semi_exterior > 0.02
                else table_G34_lookup(
                    climate_zone,
                    SCC.SEMI_EXTERIOR,
                    "SKYLIGHT",
                    skylit_wwr=0.03,
                )
            )

            return {
                "surface_conditioning_category_dict_b": get_surface_conditioning_category_dict(
                    climate_zone, building_b
                ),
                # at this point, target_u_factor_mixed should be same regardless of
                # residential <2% or >2%, skylight.
                "target_u_factor_res_b": target_u_factor_res["u_value"],
                "target_u_factor_nonres_b": target_u_factor_nonres["u_value"],
                "target_u_factor_semiheated_b": target_u_factor_semiheated["u_value"],
            }

        def list_filter(self, context_item, data=None):
            # context_item shall be the list of the list_path element
            surface_b = context_item.baseline
            # roof with subsurfaces, and the roof is not unregulated
            return (
                get_opaque_surface_type(surface_b) == OST.ROOF
                and surface_b.get("subsurfaces", None)
                and data["surface_conditioning_category_dict_b"][surface_b["id"]]
                != SCC.UNREGULATED
            )

        class RoofRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule37.BuildingRule.RoofRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    each_rule=Section5Rule37.BuildingRule.RoofRule.SubsurfaceRule(),
                    index_rmr="baseline",
                    list_path="subsurfaces[*]",
                )

            def create_data(self, context, data=None):
                surface_b = context.baseline
                scc_type = data["surface_conditioning_category_dict_b"][surface_b["id"]]
                return {"scc_type": scc_type}

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule37.BuildingRule.RoofRule.SubsurfaceRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                        manual_check_required_msg=MANUAL_CHECK_APPLICABLE,
                        required_fields={
                            "$": [
                                "classification",
                                "glazed_area",
                                "opaque_area",
                                "u_factor",
                            ]
                        },
                    )

                def is_applicable(self, context, data=None):
                    subsurface_b = context.baseline
                    return (
                        subsurface_b["classification"] != DOOR
                        or subsurface_b["glazed_area"] <= subsurface_b["opaque_area"]
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.baseline
                    subsurface_b_u_factor = subsurface_b["u_factor"]

                    scc_type = data["scc_type"]
                    target_u_factor_res_b = data["target_u_factor_res_b"]
                    target_u_factor_nonres_b = data["target_u_factor_nonres_b"]
                    target_u_factor_semiheated_b = data["target_u_factor_semiheated_b"]
                    target_u_factor = ZERO.U_FACTOR
                    if (
                        scc_type == SCC.EXTERIOR_MIXED
                        or scc_type == SCC.EXTERIOR_RESIDENTIAL
                    ):
                        target_u_factor = target_u_factor_res_b
                    elif scc_type == SCC.EXTERIOR_NON_RESIDENTIAL:
                        target_u_factor = target_u_factor_nonres_b
                    else:
                        target_u_factor = target_u_factor_semiheated_b

                    return {
                        "subsurface_b_u_factor": CalcQ(
                            "thermal_transmittance", subsurface_b_u_factor
                        ),
                        "target_u_factor": CalcQ(
                            "thermal_transmittance", target_u_factor
                        ),
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    subsurface_b_u_factor = calc_vals["subsurface_b_u_factor"]
                    target_u_factor = calc_vals["target_u_factor"]
                    return std_le(std_val=target_u_factor, val=subsurface_b_u_factor)
