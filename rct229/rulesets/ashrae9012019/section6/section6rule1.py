from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.data_fns.table_G3_7_fns import table_G3_7_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_8_fns import table_G3_8_lookup
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.schema.schema_enums import SchemaEnums

SpaceFunctionOptions = SchemaEnums.schema_enums["SpaceFunctionOptions"]
NA_SPACE_FUNCTIONS = [
    SpaceFunctionOptions.CRAWL_SPACE,
    SpaceFunctionOptions.INTERSTITIAL_SPACE,
    SpaceFunctionOptions.PLENUM,
]

CASE1_WARNING = "The baseline model included at least one plenum, crawlspace, or interstitial space with lighting power. Unable to determine whether these spaces should be included in the check."
CASE3_WARNING = "Project passes based on space-by-space method. Verify if project uses the space-by-space method."
CASE4_WARNING = "Project fails based on space-by-space method. The lighting building area type is not known to determine building area method allowance."
CASE5_WARNING = "Project passes based on building area method. Verify if project uses the building area method."
CASE6_WARNING = "Project fails based on building area method. Lighting space type is not known in all spaces to determine space-by-space method allowance."
CASE7_WARNING = "The baseline lighting building area type is not known and lighting space types are not known for all spaces to determine allowance."


class PRM9012019Rule99c05(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule99c05, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule99c05.BuildingSegmentRule(),
            index_rmd=PROPOSED,
            id="6-1",
            description="The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8",
            ruleset_section_title="Lighting",
            standard_section="Section G1.2.1(b) Mandatory Provisions related to interior lighting power",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0/buildings/0/building_segments",
        )

    class BuildingSegmentRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule99c05.BuildingSegmentRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={"$.zones[*]": ["volume"]},
                precision={
                    "building_segment_design_lighting_wattage_area": {
                        "precision": 0.01,
                        "unit": "W",
                    },
                    "building_segment_design_lighting_wattage_space": {
                        "precision": 0.01,
                        "unit": "W",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            building_segment_p = context.PROPOSED

            allowable_lpd_bam = (
                table_G3_8_lookup(building_segment_p["lighting_building_area_type"])[
                    "lpd"
                ]
                if building_segment_p.get("lighting_building_area_type") is not None
                else None
            )

            # Track plenum / crawl / interstitial spaces with lighting
            has_crawl_interstitial_plenum_with_lighting = False

            building_segment_design_lighting_wattage = ZERO.POWER
            total_building_segment_area_p = ZERO.AREA
            check_bam_flag = False
            allowable_lighting_wattage_sbs = ZERO.POWER
            for zone_p in find_all("$.zones[*]", building_segment_p):
                zone_avg_height = zone_p["volume"] / sum(
                    find_all("$.spaces[*].floor_area", zone_p)
                )

                for space_p in find_all("$.spaces[*]", zone_p):
                    space_total_lpd = sum(
                        find_all("$.interior_lighting[*].power_per_area", space_p),
                        ZERO.POWER_PER_AREA,
                    )
                    space_total_wattage = space_total_lpd * space_p["floor_area"]

                    # Always add modeled lighting wattage
                    building_segment_design_lighting_wattage += space_total_wattage

                    # Handle crawlspace / interstitial / plenum
                    space_function = space_p.get("function")
                    if space_function in NA_SPACE_FUNCTIONS:
                        if space_total_lpd > ZERO.POWER_PER_AREA:
                            has_crawl_interstitial_plenum_with_lighting = True
                        # Conservative exclusion from allowances
                        continue

                    lighting_space_type = space_p.get("lighting_space_type")

                    # Handle unoccupiable spaces (e.g. elevator / mechanical shafts)
                    if lighting_space_type == "NONE":
                        # Excluded from BAM and SBS calculations
                        continue

                    # BAM area accumulation (applicable spaces only)
                    if allowable_lpd_bam is not None:
                        total_building_segment_area_p += space_p["floor_area"]

                    # SBS handling
                    if lighting_space_type is None:
                        check_bam_flag = True
                    else:
                        allowable_lpd_space = table_G3_7_lookup(
                            lighting_space_type,
                            space_height=zone_avg_height,
                            space_area=space_p["floor_area"],
                        )["lpd"]
                        allowable_lighting_wattage_sbs += (
                            allowable_lpd_space * space_p["floor_area"]
                        )

            return {
                "allowable_lpd_bam": CalcQ("power_density", allowable_lpd_bam),
                "building_segment_design_lighting_wattage": CalcQ(
                    "electric_power", building_segment_design_lighting_wattage
                ),
                "check_bam_flag": check_bam_flag,
                "total_building_segment_area_p": CalcQ(
                    "area", total_building_segment_area_p
                ),
                "allowable_lighting_wattage_sbs": CalcQ(
                    "electric_power", allowable_lighting_wattage_sbs
                ),
                "has_crawl_interstitial_plenum_with_lighting": has_crawl_interstitial_plenum_with_lighting,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            allowable_lpd_bam = calc_vals["allowable_lpd_bam"]
            check_bam_flag = calc_vals["check_bam_flag"]
            building_segment_design_lighting_wattage = calc_vals[
                "building_segment_design_lighting_wattage"
            ]
            total_building_segment_area_p = calc_vals["total_building_segment_area_p"]
            allowable_lighting_wattage_sbs = calc_vals["allowable_lighting_wattage_sbs"]
            has_na_lighting = calc_vals["has_crawl_interstitial_plenum_with_lighting"]

            # Any crawl / plenum / interstitial space with lighting
            if has_na_lighting:
                return True

            allowable_lighting_wattage_bam = (
                allowable_lpd_bam * total_building_segment_area_p
                if allowable_lpd_bam
                else ZERO.POWER
            )

            # Case 4: Fail Space-by-Space method and unable to check Building Area method
            if not allowable_lpd_bam and not check_bam_flag and building_segment_design_lighting_wattage > allowable_lighting_wattage_sbs:
                return True

            # Case 6: Fail Building Area method and unable to check Space-by-Space method
            if allowable_lpd_bam and check_bam_flag and building_segment_design_lighting_wattage > allowable_lighting_wattage_bam:
                return True

            # Case 7: Unable to reliably check either method
            if not allowable_lpd_bam and check_bam_flag:
                return True

            return False

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            allowable_lpd_bam = calc_vals["allowable_lpd_bam"]
            check_bam_flag = calc_vals["check_bam_flag"]
            has_na_lighting = calc_vals["has_crawl_interstitial_plenum_with_lighting"]

            if has_na_lighting:
                return CASE1_WARNING
            elif not allowable_lpd_bam and not check_bam_flag:
                return CASE4_WARNING
            elif allowable_lpd_bam and check_bam_flag:
                return CASE6_WARNING
            elif not allowable_lpd_bam and check_bam_flag:
                return CASE7_WARNING
            else:
                return None

        def rule_check(self, context, calc_vals=None, data=None):
            allowable_lpd_bam = calc_vals["allowable_lpd_bam"]
            check_bam_flag = calc_vals["check_bam_flag"]
            building_segment_design_lighting_wattage = calc_vals[
                "building_segment_design_lighting_wattage"
            ]
            total_building_segment_area_p = calc_vals["total_building_segment_area_p"]
            allowable_lighting_wattage_sbs = calc_vals["allowable_lighting_wattage_sbs"]

            allowable_lpd_wattage_bam = (
                allowable_lpd_bam * total_building_segment_area_p
                if allowable_lpd_bam
                else ZERO.POWER
            )

            return (
                (allowable_lpd_bam or not check_bam_flag)
                and (
                    building_segment_design_lighting_wattage < allowable_lpd_wattage_bam
                )
                or self.precision_comparison[
                    "building_segment_design_lighting_wattage_area"
                ](building_segment_design_lighting_wattage, allowable_lpd_wattage_bam)
                or (
                    building_segment_design_lighting_wattage
                    < allowable_lighting_wattage_sbs
                    or self.precision_comparison[
                        "building_segment_design_lighting_wattage_space"
                    ](
                        building_segment_design_lighting_wattage,
                        allowable_lighting_wattage_sbs,
                    )
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            allowable_lpd_bam = calc_vals["allowable_lpd_bam"]
            check_bam_flag = calc_vals["check_bam_flag"]
            building_segment_design_lighting_wattage = calc_vals[
                "building_segment_design_lighting_wattage"
            ]
            total_building_segment_area_p = calc_vals["total_building_segment_area_p"]
            allowable_lighting_wattage_sbs = calc_vals["allowable_lighting_wattage_sbs"]

            allowable_lpd_wattage_bam = (
                allowable_lpd_bam * total_building_segment_area_p
                if allowable_lpd_bam
                else ZERO.POWER
            )

            return (
                (allowable_lpd_bam or not check_bam_flag)
                and (
                    building_segment_design_lighting_wattage < allowable_lpd_wattage_bam
                )
                or std_equal(
                    allowable_lpd_wattage_bam, building_segment_design_lighting_wattage
                )
                or (
                    building_segment_design_lighting_wattage
                    < allowable_lighting_wattage_sbs
                    or std_equal(
                        allowable_lighting_wattage_sbs,
                        building_segment_design_lighting_wattage,
                    )
                )
            )

        def get_pass_msg(self, context, calc_vals=None, data=None):
            allowable_lpd_bam = calc_vals["allowable_lpd_bam"]
            check_bam_flag = calc_vals["check_bam_flag"]

            if not allowable_lpd_bam and not check_bam_flag:
                return CASE3_WARNING
            else:
                return CASE5_WARNING

        def get_fail_msg(self, context, calc_vals=None, data=None):
            allowable_lpd_bam = calc_vals["allowable_lpd_bam"]
            check_bam_flag = calc_vals["check_bam_flag"]

            if not allowable_lpd_bam and not check_bam_flag:
                return CASE4_WARNING
            elif allowable_lpd_bam and check_bam_flag:
                return CASE6_WARNING
            elif not allowable_lpd_bam and check_bam_flag:
                return CASE7_WARNING
            else:
                return None
