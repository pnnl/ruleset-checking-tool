from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_building_scc_window_wall_ratios_dict import (
    get_building_scc_window_wall_ratios_dict,
)
from rct229.ruleset_functions.get_opaque_surface_type import OpaqueSurfaceType as OST
from rct229.ruleset_functions.get_opaque_surface_type import get_opaque_surface_type
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

DOOR = schema_enums["SubsurfaceClassificationType"].DOOR


class Section5Rule26(RuleDefinitionListIndexedBase):
    """Rule 26 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule26, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule26.BuildingRule(),
            index_rmr="baseline",
            id="5-26",
            description="Vertical fenestration SHGC shall match the appropriate requirements in Tables G3.4-1 through G3.4-8.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        climate_zone = rmr_baseline["weather"]["climate_zone"]

        # TODO It is determined that later we will modify this function to RMD level -
        # This implementation is temporary
        bldg_scc_wwr_ratio_dict = {
            building_b["id"]: get_building_scc_window_wall_ratios_dict(
                climate_zone, building_b
            )
            for building_b in find_all(self.list_path, rmr_baseline)
        }

        return {
            "climate_zone": rmr_baseline["weather"]["climate_zone"],
            "bldg_scc_wwr_ratio_dict": bldg_scc_wwr_ratio_dict,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule26.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section5Rule26.BuildingRule.AboveGradeWallRule(),
                index_rmr="baseline",
                list_path="$..surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            climate_zone = data["climate_zone"]
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
                **data,
                # TODO this function will likely need to be revised to RMD level later.
                "scc_dict_b": get_surface_conditioning_category_dict(
                    climate_zone, building_b
                ),
                "manual_check_required_flag": manual_check_required_flag,
                "target_shgc_mix": target_shgc_mix,
                "target_shgc_res": target_shgc_res,
                "target_shgc_nonres": target_shgc_nonres,
                "target_shgc_semiheated": target_shgc_semiheated,
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.baseline
            scc_dict_b = data["scc_dict_b"]
            return (get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL) and (
                scc_dict_b[surface_b["id"]] != SCC.UNREGULATED
            )

        class AboveGradeWallRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule26.BuildingRule.AboveGradeWallRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    each_rule=Section5Rule26.BuildingRule.AboveGradeWallRule.SubsurfaceRule(),
                    index_rmr="baseline",
                    list_path="subsurfaces[*]",
                    required_fields={
                        "$.subsurfaces[*]": [
                            "classification",
                            "solar_heat_gain_coefficient",
                        ]
                    },
                )

            def manual_check_required(self, context, calc_vals=None, data=None):
                scc_dict_b = data["scc_dict_b"]
                manual_check_required_flag = data["manual_check_required_flag"]
                surface_b = context.baseline
                # if exterior mixed and required manual check
                return (
                    scc_dict_b[surface_b["id"]] == SCC.EXTERIOR_MIXED
                    and manual_check_required_flag
                )

            def create_data(self, context, data=None):
                surface_b = context.baseline
                scc_dict_b = data["scc_dict_b"]
                return {**data, "scc": scc_dict_b[surface_b["id"]]}

            def list_filter(self, context_item, data=None):
                subsurface_b = context_item.baseline
                return subsurface_b["classification"] != DOOR or subsurface_b.get(
                    ["glazed_area"], 0.0
                ) > subsurface_b.get(["opaque_area"], 0.0)

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule26.BuildingRule.AboveGradeWallRule.SubsurfaceRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                    )

                def get_calc_vals(self, context, data=None):
                    scc = data["scc"]
                    subsurface_b = context.baseline
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
                    return target_shgc is not None and std_equal(
                        target_shgc, subsurface_shgc
                    )
