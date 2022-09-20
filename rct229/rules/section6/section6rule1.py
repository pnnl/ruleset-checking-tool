from rct229.data_fns.table_G3_7_fns import table_G3_7_lookup
from rct229.data_fns.table_G3_8_fns import table_G3_8_lookup
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, pint_sum
from rct229.utils.pint_utils import CalcQ, pint_sum

CASE3_WARNING = "Project passes based on space-by-space method. Verify if project sues space-by-space method."
CASE4_WARNING = "Project fails based on space-by-space method. LIGHTING_BUILDING_AREA_TYPE is not known to determine building area method allowance."
CASE5_WARNING = "Project passes based on building area method. Verify if project uses building area method."
CASE6_WARNING = "Project fails based on building area method. LIGHTING_SPACE_TYPE is not known in all spaces to determine space-by-space method allowance."
CASE7_WARNING = "LIGHTING_BUILDING_AREA_TYPE is not known and LIGHTING_SPACE_TYPE is not known in all spaces to determine allowance."



class Section6Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule1, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section6Rule1.BuildingSegmentRule(),
            index_rmr="proposed",
            id="6-1",
            description="The total building interior lighting power shall not exceed the interior lighting power "
            "allowance determined using either Table G3.7 or G3.8",
            list_path="ruleset_model_instances[0].buildings[*].building_segments[*]",
        )

    class BuildingSegmentRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule1.BuildingSegmentRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                each_rule=Section6Rule1.BuildingSegmentRule.ZoneRule(),
                index_rmr="proposed",
                list_path="$..zones[*]",
            )

        def create_data(self, context, data):
            building_segment_p = context.proposed

            return {
                "allowable_LPD_BAM": table_G3_8_lookup(
                    building_segment_p["lighting_building_area_type"]
                )["lpd"] if building_segment_p.get("lighting_building_area_type") != None else ZERO.POWER_PER_AREA,
                "building_area_type_bool": True if building_segment_p.get("lighting_building_area_type") != None else False
                "building_allowable_lighting_power": CalcQ(
                    "electric_power", building_allowable_lighting_power
                ),
                "building_design_lighting_power": CalcQ(
                    "electric_power", building_design_lighting_power
                ),


        class ZoneRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section6Rule1.BuildingSegmentRule.ZoneRule, self,).__init__(
                    rmrs_used=UserBaselineProposedVals(False, False, True),
                    each_rule=Section6Rule1.BuildingSegmentRule.ZoneRule.SpaceRule(),
                    index_rmr="proposed",
                    list_path="$..spaces[*]",
                    required_fields={"$": ["volume"]},
                )

            def create_data(self, context, data):
                zone_p = context.proposed
                floor_area_p = pint_sum(
                    find_all("spaces[*].floor_area", zone_p), ZERO.AREA
                )

                return {
                    "floor_area_p": floor_area_p,
                    "avg_space_height": zone_p.get("volume", ZERO.VOLUME)
                    / floor_area_p,
                }

            class SpaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section6Rule1.BuildingSegmentRule.ZoneRule.SpaceRule, self
                    ).__init__(rmrs_used=UserBaselineProposedVals(False, False, True))

                def get_calc_vals(self, context, data=None):
                    space_p = context.proposed
                    allowable_LPD_BAM = data["allowable_LPD_BAM"]
                    avg_space_height = data["avg_space_height"]
                    floor_area_p = data["floor_area_p"]
                    building_area_type_bool = data["building_area_type_bool"]

                    building_segment_design_lighting_wattage = (
                        pint_sum(
                            find_all("$..interior_lighting[*].power_per_area", space_p),
                            ZERO.POWER_PER_AREA,
                        )
                        * space_p["floor_area"]
                    )

                    total_building_segment_area_p = ZERO.AREA
                    if building_area_type_bool != None:
                        total_building_segment_area_p += space_p["floor_area"]

                    check_BAM_flag = False
                    allowable_LPD_space = ZERO.POWER_PER_AREA
                    allowable_lighting_wattage_SBS = ZERO.POWER
                    if space_p.get("lighting_space_type") == None:
                        check_BAM_flag = True
                    else:
                        allowable_LPD_space = table_G3_7_lookup(
                            space_p.get("lighting_space_type"),
                            avg_space_height,
                            floor_area_p,
                        )["lpd"]
                        allowable_lighting_wattage_SBS += (
                            allowable_LPD_space * space_p["floor_area"]
                        )

                    return {
                        "allowable_LPD_BAM": allowable_LPD_BAM,
                        "building_segment_design_lighting_wattage": building_segment_design_lighting_wattage,
                        "check_BAM_flag": check_BAM_flag,
                        "total_building_segment_area_p": total_building_segment_area_p,
                        "allowable_LPD_space": allowable_LPD_space,
                        "allowable_lighting_wattage_SBS": allowable_lighting_wattage_SBS,
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    allowable_LPD_BAM = calc_vals["allowable_LPD_BAM"]
                    check_BAM_flag = calc_vals["check_BAM_flag"]
                    building_segment_design_lighting_wattage = calc_vals[
                        "building_segment_design_lighting_wattage"
                    ]
                    total_building_segment_area_p = calc_vals[
                        "total_building_segment_area_p"
                    ]
                    allowable_lighting_wattage_SBS = calc_vals[
                        "allowable_lighting_wattage_SBS"
                    ]

                    if allowable_LPD_BAM and not check_BAM_flag:
                        if building_segment_design_lighting_wattage <= max(
                            allowable_LPD_BAM * total_building_segment_area_p,
                            allowable_lighting_wattage_SBS,
                        ):
                            return True
                        else:
                            return False
                    elif not (allowable_LPD_BAM and check_BAM_flag):
                        if (
                            building_segment_design_lighting_wattage
                            <= allowable_lighting_wattage_SBS
                        ):
                            return True
                        else:
                            return False
                    elif allowable_LPD_BAM and check_BAM_flag:
                        if (
                            building_segment_design_lighting_wattage
                            <= allowable_LPD_BAM * total_building_segment_area_p
                        ):
                            return True
                        else:
                            return False
                    else:
                        return False

                def get_pass_msg(self, context, calc_vals=None, data=None):
                    allowable_LPD_BAM = calc_vals["allowable_LPD_BAM"]
                    check_BAM_flag = calc_vals["check_BAM_flag"]

                    if allowable_LPD_BAM and not check_BAM_flag:
                        return ""
                    elif not allowable_LPD_BAM and not check_BAM_flag:
                        return CASE3_WARNING
                    else:
                        return CASE5_WARNING

                def get_fail_msg(self, context, calc_vals=None, data=None):
                    allowable_LPD_BAM = calc_vals["allowable_LPD_BAM"]
                    check_BAM_flag = calc_vals["check_BAM_flag"]

                    if allowable_LPD_BAM and not check_BAM_flag:
                        return ""
                    elif not allowable_LPD_BAM and not check_BAM_flag:
                        return CASE4_WARNING
                    elif allowable_LPD_BAM and check_BAM_flag:
                        return CASE6_WARNING
                    elif not allowable_LPD_BAM and check_BAM_flag:
                        return CASE7_WARNING
                    