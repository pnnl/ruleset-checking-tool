from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_scc_window_wall_ratios_dict import (
    get_building_scc_window_wall_ratios_dict,
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
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
MANUAL_CHECK_REQUIRED_MSG = "Manual review is requested to verify vertical fenestration meets SHGC requirement as per Table G3.4. "


class PRM9012019Rule96n40(RuleDefinitionListIndexedBase):
    """Rule 20 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule96n40, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule96n40.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-20",
            description="Vertical fenestration SHGC shall match the appropriate requirements in Tables G3.4-1 through G3.4-8.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(d) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmd_baseline = context.BASELINE_0
        climate_zone = rmd_baseline["ruleset_model_descriptions"][0]["weather"][
            "climate_zone"
        ]
        constructions = rmd_baseline["ruleset_model_descriptions"][0].get(
            "constructions"
        )

        # TODO It is determined that later we will modify this function to RMD level -
        # This implementation is temporary
        bldg_scc_wwr_ratio_dict = {
            building_b["id"]: get_building_scc_window_wall_ratios_dict(
                climate_zone, constructions, building_b
            )
            for building_b in find_all(self.list_path, rmd_baseline)
        }

        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
            "bldg_scc_wwr_ratio_dict": bldg_scc_wwr_ratio_dict,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule96n40.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule96n40.BuildingRule.AboveGradeWallRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            climate_zone = data["climate_zone"]
            constructions = data["constructions"]
            bldg_scc_wwr_ratio = data["bldg_scc_wwr_ratio_dict"][building_b["id"]]
            # manual flag required?
            manual_check_required_flag = bldg_scc_wwr_ratio[
                SCC.EXTERIOR_MIXED
            ] > 0 and not (
                (
                    table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=0.1,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=10.1,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=20.1,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=30.1,
                    )["solar_heat_gain_coefficient"]
                )
                and (
                    table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=0.1,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=10.1,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=20.1,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=30.1,
                    )["solar_heat_gain_coefficient"]
                )
                and (
                    table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=0.1,
                    )["solar_heat_gain_coefficient"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=0.1,
                    )["solar_heat_gain_coefficient"]
                )
            )
            # get standard code data
            target_shgc_mix = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_RESIDENTIAL,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.EXTERIOR_MIXED],
                )["solar_heat_gain_coefficient"]
                if bldg_scc_wwr_ratio[SCC.EXTERIOR_MIXED] > 0
                else None
            )
            target_shgc_res = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_RESIDENTIAL,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.EXTERIOR_RESIDENTIAL],
                )["solar_heat_gain_coefficient"]
                if bldg_scc_wwr_ratio[SCC.EXTERIOR_RESIDENTIAL] > 0
                else None
            )
            target_shgc_nonres = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.EXTERIOR_NON_RESIDENTIAL],
                )["solar_heat_gain_coefficient"]
                if bldg_scc_wwr_ratio[SCC.EXTERIOR_NON_RESIDENTIAL] > 0
                else None
            )
            target_shgc_semiheated = (
                table_G34_lookup(
                    climate_zone,
                    SCC.SEMI_EXTERIOR,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.SEMI_EXTERIOR],
                )["solar_heat_gain_coefficient"]
                if bldg_scc_wwr_ratio[SCC.SEMI_EXTERIOR] > 0
                else None
            )
            return {
                # TODO this function will likely need to be revised to RMD level later.
                "scc_dict_b": get_surface_conditioning_category_dict(
                    climate_zone, building_b, constructions
                ),
                "manual_check_required_flag": manual_check_required_flag,
                "target_shgc_mix": target_shgc_mix,
                "target_shgc_res": target_shgc_res,
                "target_shgc_nonres": target_shgc_nonres,
                "target_shgc_semiheated": target_shgc_semiheated,
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            scc_dict_b = data["scc_dict_b"]
            return (
                (get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL)
                and (scc_dict_b[surface_b["id"]] != SCC.UNREGULATED)
                and len(surface_b.get("subsurfaces", [])) > 0
            )

        class AboveGradeWallRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule96n40.BuildingRule.AboveGradeWallRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    each_rule=PRM9012019Rule96n40.BuildingRule.AboveGradeWallRule.SubsurfaceRule(),
                    index_rmd=BASELINE_0,
                    list_path="subsurfaces[*]",
                    required_fields={
                        "$.subsurfaces[*]": [
                            "classification",
                            "solar_heat_gain_coefficient",
                        ]
                    },
                    manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                )

            def create_data(self, context, data=None):
                surface_b = context.BASELINE_0
                scc_dict_b = data["scc_dict_b"]
                return {"scc": scc_dict_b[surface_b["id"]]}

            def list_filter(self, context_item, data=None):
                subsurface_b = context_item.BASELINE_0
                return subsurface_b["classification"] != DOOR or subsurface_b.get(
                    ["glazed_area"], ZERO.AREA
                ) > subsurface_b.get(["opaque_area"], ZERO.AREA)

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        PRM9012019Rule96n40.BuildingRule.AboveGradeWallRule.SubsurfaceRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                        precision={
                            "subsurface_shgc_b": {
                                "precision": 0.01,
                                "unit": "",
                            }
                        },
                    )

                def manual_check_required(self, context, calc_vals=None, data=None):
                    manual_check_required_flag = data["manual_check_required_flag"]
                    # if exterior mixed and required manual check
                    return (
                        data["scc"] == SCC.EXTERIOR_MIXED and manual_check_required_flag
                    )

                def get_calc_vals(self, context, data=None):
                    scc = data["scc"]
                    subsurface_b = context.BASELINE_0
                    target_shgc = 0.0
                    if scc == SCC.EXTERIOR_MIXED:
                        target_shgc = data["target_shgc_mix"]
                    elif scc == SCC.EXTERIOR_RESIDENTIAL:
                        target_shgc = data["target_shgc_res"]
                    elif scc == SCC.EXTERIOR_NON_RESIDENTIAL:
                        target_shgc = data["target_shgc_nonres"]
                    elif scc == SCC.SEMI_EXTERIOR:
                        target_shgc = data["target_shgc_semiheated"]
                    else:
                        assert f"Severe Error: No matching surface category for: {scc}"
                    return {
                        "subsurface_shgc": subsurface_b["solar_heat_gain_coefficient"],
                        "target_shgc": target_shgc,
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    target_shgc = calc_vals["target_shgc"]
                    subsurface_shgc = calc_vals["subsurface_shgc"]

                    return target_shgc is not None and self.precision_comparison[
                        "subsurface_shgc_b"
                    ](subsurface_shgc, target_shgc)

                def is_tolerance_fail(self, context, calc_vals=None, data=None):
                    target_shgc = calc_vals["target_shgc"]
                    subsurface_shgc = calc_vals["subsurface_shgc"]
                    return target_shgc is not None and std_equal(
                        std_val=target_shgc, val=subsurface_shgc
                    )
