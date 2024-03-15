from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import RMT
from rct229.rulesets.ashrae9012019.data_fns.table_G3_7_fns import table_G3_7_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_8_fns import table_G3_8_lookup
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ

CASE3_WARNING = "Project passes based on space-by-space method. Verify if project sues space-by-space method."
CASE4_WARNING = "Project fails based on space-by-space method. LIGHTING_BUILDING_AREA_TYPE is not known to determine building area method allowance."
CASE5_WARNING = "Project passes based on building area method. Verify if project uses building area method."
CASE6_WARNING = "Project fails based on building area method. LIGHTING_SPACE_TYPE is not known in all spaces to determine space-by-space method allowance."
CASE7_WARNING = "LIGHTING_BUILDING_AREA_TYPE is not known and LIGHTING_SPACE_TYPE is not known in all spaces to determine allowance."


class Section6Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule1, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section6Rule1.BuildingSegmentRule(),
            index_rmr=RMT.PROPOSED,
            id="6-1",
            description="The total building interior lighting power shall not exceed the interior lighting power "
            "allowance determined using either Table G3.7 or G3.8",
            ruleset_section_title="Lighting",
            standard_section="Section G1.2.1(b) Mandatory Provisions related to interior lighting power",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0/buildings/0/building_segments",
        )

    class BuildingSegmentRule(RuleDefinitionBase):
        def __init__(self):
            super(Section6Rule1.BuildingSegmentRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={"$.zones[*]": ["volume"]},
            )

        def get_calc_vals(self, context, data=None):
            building_segment_p = context.PROPOSED

            allowable_LPD_BAM = (
                table_G3_8_lookup(building_segment_p["lighting_building_area_type"])[
                    "lpd"
                ]
                if building_segment_p.get("lighting_building_area_type") != None
                else None
            )

            building_segment_design_lighting_wattage = ZERO.POWER
            total_building_segment_area_p = ZERO.AREA
            check_BAM_flag = False
            allowable_lighting_wattage_SBS = ZERO.POWER
            for zone_p in find_all("$.zones[*]", building_segment_p):
                zone_avg_height = zone_p["volume"] / sum(
                    find_all("$.spaces[*].floor_area", zone_p)
                )

                for space_p in find_all("$.spaces[*]", zone_p):
                    building_segment_design_lighting_wattage += (
                        sum(
                            find_all("$.interior_lighting[*].power_per_area", space_p),
                            ZERO.POWER_PER_AREA,
                        )
                        * space_p["floor_area"]
                    )

                    if allowable_LPD_BAM != None:
                        total_building_segment_area_p += space_p["floor_area"]

                    lighting_space_type = space_p.get("lighting_space_type")
                    if lighting_space_type is None:
                        check_BAM_flag = True
                    else:
                        allowable_LPD_space = table_G3_7_lookup(
                            lighting_space_type,
                            space_height=zone_avg_height,
                            space_area=space_p["floor_area"],
                        )["lpd"]
                        allowable_lighting_wattage_SBS += (
                            allowable_LPD_space * space_p["floor_area"]
                        )

            return {
                "allowable_LPD_BAM": CalcQ("power_density", allowable_LPD_BAM),
                "building_segment_design_lighting_wattage": CalcQ(
                    "electric_power", building_segment_design_lighting_wattage
                ),
                "check_BAM_flag": check_BAM_flag,
                "total_building_segment_area_p": CalcQ(
                    "area", total_building_segment_area_p
                ),
                "allowable_lighting_wattage_SBS": CalcQ(
                    "electric_power", allowable_lighting_wattage_SBS
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            allowable_LPD_BAM = calc_vals["allowable_LPD_BAM"]
            check_BAM_flag = calc_vals["check_BAM_flag"]
            building_segment_design_lighting_wattage = calc_vals[
                "building_segment_design_lighting_wattage"
            ]
            total_building_segment_area_p = calc_vals["total_building_segment_area_p"]
            allowable_lighting_wattage_SBS = calc_vals["allowable_lighting_wattage_SBS"]

            allowable_LPD_wattage_BAM = (
                allowable_LPD_BAM * total_building_segment_area_p
                if allowable_LPD_BAM
                else ZERO.POWER
            )

            return (
                (allowable_LPD_BAM or not check_BAM_flag)
                and building_segment_design_lighting_wattage
                <= allowable_LPD_wattage_BAM
                or building_segment_design_lighting_wattage
                <= allowable_lighting_wattage_SBS
            )

        def get_pass_msg(self, context, calc_vals=None, data=None):
            allowable_LPD_BAM = calc_vals["allowable_LPD_BAM"]
            check_BAM_flag = calc_vals["check_BAM_flag"]

            if not allowable_LPD_BAM and not check_BAM_flag:
                return CASE3_WARNING
            else:
                return CASE5_WARNING

        def get_fail_msg(self, context, calc_vals=None, data=None):
            allowable_LPD_BAM = calc_vals["allowable_LPD_BAM"]
            check_BAM_flag = calc_vals["check_BAM_flag"]

            if not allowable_LPD_BAM and not check_BAM_flag:
                return CASE4_WARNING
            elif allowable_LPD_BAM and check_BAM_flag:
                return CASE6_WARNING
            elif not allowable_LPD_BAM and check_BAM_flag:
                return CASE7_WARNING
