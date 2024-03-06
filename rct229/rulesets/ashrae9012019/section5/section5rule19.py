from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
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
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
MANUAL_CHECK_REQUIRED_MSG = "Manual review is requested to verify vertical fenestration meets U-factor requirement as per Table G3.4. "


class Section5Rule19(RuleDefinitionListIndexedBase):
    """Rule 24 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule19, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule19.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-19",
            description="Vertical fenestration U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8 for the appropriate WWR in the baseline RMD.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(d) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.BASELINE_0
        climate_zone = rmr_baseline["weather"]["climate_zone"]

        # TODO It is determined later we will modify this function to RMD level -
        # The implementation is temporary
        bldg_scc_wwr_ratio_dict = {}
        for building_b in find_all(self.list_path, rmr_baseline):
            bldg_scc_wwr_ratio_dict[
                building_b["id"]
            ] = get_building_scc_window_wall_ratios_dict(climate_zone, building_b)

        return {
            "climate_zone": rmr_baseline["weather"]["climate_zone"],
            "bldg_scc_wwr_ratio_dict": bldg_scc_wwr_ratio_dict,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule19.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section5Rule19.BuildingRule.AboveGradeWallRule(),
                index_rmr=BASELINE_0,
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
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
                    )["u_value"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=10.1,
                    )["u_value"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=20.1,
                    )["u_value"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=30.1,
                    )["u_value"]
                )
                and (
                    table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=0.1,
                    )["u_value"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=10.1,
                    )["u_value"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=20.1,
                    )["u_value"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=30.1,
                    )["u_value"]
                )
                and (
                    table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=0.1,
                    )["u_value"]
                    == table_G34_lookup(
                        climate_zone,
                        SCC.EXTERIOR_NON_RESIDENTIAL,
                        "VERTICAL GLAZING",
                        wwr=0.1,
                    )["u_value"]
                )
            )
            # get standard code data
            target_u_factor_mix = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_RESIDENTIAL,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.EXTERIOR_MIXED],
                )["u_value"]
                if bldg_scc_wwr_ratio[SCC.EXTERIOR_MIXED] > 0
                else ZERO.U_FACTOR
            )
            target_u_factor_res = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_RESIDENTIAL,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.EXTERIOR_RESIDENTIAL],
                )["u_value"]
                if bldg_scc_wwr_ratio[SCC.EXTERIOR_RESIDENTIAL] > 0
                else ZERO.U_FACTOR
            )
            target_u_factor_nonres = (
                table_G34_lookup(
                    climate_zone,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.EXTERIOR_NON_RESIDENTIAL],
                )["u_value"]
                if bldg_scc_wwr_ratio[SCC.EXTERIOR_NON_RESIDENTIAL] > 0
                else ZERO.U_FACTOR
            )
            target_u_factor_semiheated = (
                table_G34_lookup(
                    climate_zone,
                    SCC.SEMI_EXTERIOR,
                    "VERTICAL GLAZING",
                    wwr=bldg_scc_wwr_ratio[SCC.SEMI_EXTERIOR],
                )["u_value"]
                if bldg_scc_wwr_ratio[SCC.SEMI_EXTERIOR] > 0
                else ZERO.U_FACTOR
            )

            return {
                # TODO this function will likely need to be revised to RMD level later.
                "scc_dict_b": get_surface_conditioning_category_dict(
                    climate_zone, building_b
                ),
                "manual_check_required_flag": manual_check_required_flag,
                "target_u_factor_mix": target_u_factor_mix,
                "target_u_factor_res": target_u_factor_res,
                "target_u_factor_nonres": target_u_factor_nonres,
                "target_u_factor_semiheated": target_u_factor_semiheated,
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0
            scc_dict_b = data["scc_dict_b"]
            return (get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL) and (
                scc_dict_b[surface_b["id"]] != SCC.UNREGULATED
            )

        class AboveGradeWallRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule19.BuildingRule.AboveGradeWallRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    each_rule=Section5Rule19.BuildingRule.AboveGradeWallRule.SubsurfaceRule(),
                    index_rmr=BASELINE_0,
                    list_path="subsurfaces[*]",
                    required_fields={
                        "$.subsurfaces[*]": [
                            "classification",
                            "glazed_area",
                            "opaque_area",
                            "u_factor",
                        ]
                    },
                    manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                )

            def manual_check_required(self, context, calc_vals=None, data=None):
                scc_dict_b = data["scc_dict_b"]
                manual_check_required_flag = data["manual_check_required_flag"]
                surface_b = context.BASELINE_0
                # if exterior mixed and required manual check
                return (
                    scc_dict_b[surface_b["id"]] == SCC.EXTERIOR_MIXED
                    and manual_check_required_flag
                )

            def create_data(self, context, data=None):
                surface_b = context.BASELINE_0
                scc_dict_b = data["scc_dict_b"]
                return {"scc": scc_dict_b[surface_b["id"]]}

            def list_filter(self, context_item, data=None):
                subsurface_b = context_item.BASELINE_0
                return (
                    subsurface_b["classification"] != DOOR
                    or subsurface_b["glazed_area"] > subsurface_b["opaque_area"]
                )

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule19.BuildingRule.AboveGradeWallRule.SubsurfaceRule,
                        self,
                    ).__init__(
                        rmrs_used=produce_ruleset_model_instance(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.BASELINE_0
                    scc = data["scc"]
                    target_u_factor = None
                    if scc == SCC.EXTERIOR_MIXED:
                        target_u_factor = data["target_u_factor_mix"]
                    elif scc == SCC.EXTERIOR_RESIDENTIAL:
                        target_u_factor = data["target_u_factor_res"]
                    elif scc == SCC.EXTERIOR_NON_RESIDENTIAL:
                        target_u_factor = data["target_u_factor_nonres"]
                    elif scc == SCC.SEMI_EXTERIOR:
                        target_u_factor = data["target_u_factor_semiheated"]
                    else:
                        assert (
                            False
                        ), f"Severe Error: No matching surface category for: {scc}"

                    return {
                        "target_u_factor": CalcQ(
                            "thermal_transmittance", target_u_factor
                        ),
                        "subsurface_u_factor": CalcQ(
                            "thermal_transmittance", subsurface_b["u_factor"]
                        ),
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    target_u_factor = calc_vals["target_u_factor"]
                    subsurface_u_factor = calc_vals["subsurface_u_factor"]
                    return std_equal(std_val=target_u_factor, val=subsurface_u_factor)
