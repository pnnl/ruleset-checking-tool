from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one

LIGHTING_SPACE = schema_enums["LightingSpaceType2019ASHRAE901TG37"]
LIGHTING_BUILDING_AREA = schema_enums[
    "LightingBuildingAreaOptions2019ASHRAE901T951TG38"
]


UNDETERMINED_MSG = "It is not clear from the RMD if <insert space.id> is a dwelling unit. If it is a dwelling unit it is required that it be modeled following the rule that for baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity design day cooling schedules shalled be modeled using an equipment hourly schedule that is the same as the most used hourly weekday schedule from the annual simulation. This rule <insert 'was' if all(inf_pass_cooling,occ_pass_cooling,int_lgt_pass_cooling,misc_pass_cooling) == true and insert 'was not' if all(inf_pass_cooling,occ_pass_cooling,int_lgt_pass_cooling,misc_pass_cooling) == false> followed for this space if applicable."
FAIL_MSG = "<insert space.id> does not appear to have been modeled following the rule that for baseline cooling sizing runs in residential dwelling units hourly schedules shall be the same as the most used hourly weekday schedule from the annual simulation for the following schedules: <include 'infiltration' if inf_pass_cooling == false> , <include 'occupants' if occ_pass_cooling == false>, <include 'lighting' if int_lgt_pass_cooling == false>, <include 'gas and/or electricity miscellaneous' if misc_pass_cooling ==  false>."


class Section19Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule4, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule4.BuildingSegmentRule(),
            index_rmr="baseline",
            id="19-4",
            description="For baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity using equipment hourly schedule shall be the same as the most used hourly weekday schedule from the annual simulation.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1 Exception",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*]",
        )

    class BuildingSegmentRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section19Rule4.BuildingSegmentRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section19Rule4.BuildingSegmentRule.SpaceRule(),
                index_rmr="baseline",
                list_path="$.zones[*].spaces[*]",
            )

        def create_data(self, context, data):
            building_segment_b = context.baseline

            bldg_type_b = building_segment_b.get("lighting_building_area_type")

            bldg_area_is_defined = False
            building_area_is_MF_dormitory_or_hotel = False
            if not bldg_type_b:
                bldg_area_is_defined = True
            elif bldg_type_b in [
                LIGHTING_BUILDING_AREA.DORMITORY,
                LIGHTING_BUILDING_AREA.HOTEL_MOTEL,
                LIGHTING_BUILDING_AREA.MULTIFAMILY,
            ]:
                building_area_is_MF_dormitory_or_hotel = True

            return {
                "bldg_area_is_defined": bldg_area_is_defined,
                "building_area_is_MF_dormitory_or_hotel": building_area_is_MF_dormitory_or_hotel,
            }

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section19Rule4.BuildingSegmentRule.SpaceRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def is_applicable(self, context, data=None):
                return True

            def get_calc_vals(self, context, data=None):
                space_b = context.baseline

                bldg_area_is_defined = False
                building_area_is_MF_dormitory_or_hotel = False
                space_lighting_or_vent_space_type_is_defined = False
                space_lighting_space_type_is_dwelling_unit = False

                if (
                    space_b.get("lighting_space_type ") is None
                    and space_b.get("ventilation_space_type") is None
                ):
                    space_lighting_or_vent_space_type_is_defined = False

                # check the  occupancy schedule
                occ_pass_cooling = True
                multiplier_sch = space_b["occupant_multiplier_schedule"]

                design_cooling_multiplier_sch = get_most_used_weekday_hourly_schedule(
                    multiplier_sch["cooling_design_day_sequence"]
                )

                most_used_weekday_hourly_schedule = (
                    get_most_used_weekday_hourly_schedule(multiplier_sch)
                )

                for idx, x in enumerate(design_cooling_multiplier_sch):
                    if most_used_weekday_hourly_schedule[idx] != x:
                        occ_pass_cooling = False
                        break

                # check the interior lighting
                lgting_obj_list = space_b["interior_lighting"]

                int_lgt_pass_cooling = True

                multiplier_sch = space_b["lighting_multiplier_schedule"]
                design_cooling_multiplier_sch = multiplier_sch[
                    "cooling_design_day_sequence"
                ]
                most_used_weekday_hourly_schedule = (
                    get_most_used_weekday_hourly_schedule(multiplier_sch)
                )

                for idx, x in enumerate(design_cooling_multiplier_sch):
                    if most_used_weekday_hourly_schedule[idx] != x:
                        int_lgt_pass_cooling = False
                        break

                # check the misc equipment
                misc_obj_list = space_b["miscellaneous_equipment"]

                misc_pass_cooling = True

                multiplier_sch = space_b["multiplier_schedule"]
                design_cooling_multiplier_sch = multiplier_sch[
                    "cooling_design_day_sequence"
                ]

                most_used_weekday_hourly_schedule = (
                    get_most_used_weekday_hourly_schedule(design_cooling_multiplier_sch)
                )
                for idx, x in enumerate(design_cooling_multiplier_sch):
                    if most_used_weekday_hourly_schedule[idx] != x:
                        misc_pass_cooling = False
                        break

                return True

            def manual_check_required(self, context, calc_vals=None, data=None):
                space_lighting_or_vent_space_type_is_defined = data[
                    "space_lighting_or_vent_space_type_is_defined"
                ]
                bldg_area_is_defined = data["bldg_area_is_defined"]
                building_area_is_MF_dormitory_or_hotel = data[
                    "building_area_is_MF_dormitory_or_hotel"
                ]

                return not space_lighting_or_vent_space_type_is_defined and (
                    not bldg_area_is_defined or building_area_is_MF_dormitory_or_hotel
                )

            def rule_check(self, context, calc_vals=None, data=None):
                return True

            def get_fail_msg(self, context, calc_vals=None, data=None):
                space_lighting_space_type_is_dwelling_unit = data[
                    "space_lighting_space_type_is_dwelling_unit"
                ]
                inf_pass_cooling = data["inf_pass_cooling"]
                occ_pass_cooling = data["occ_pass_cooling"]
                int_lgt_pass_cooling = data["int_lgt_pass_cooling"]
                misc_pass_cooling = data["misc_pass_cooling"]

                return space_lighting_space_type_is_dwelling_unit and all(
                    [
                        inf_pass_cooling,
                        occ_pass_cooling,
                        int_lgt_pass_cooling,
                        misc_pass_cooling,
                    ]
                )
