from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_most_used_weekday_hourly_schedule import (
    get_most_used_weekday_hourly_schedule,
)


LIGHTING_SPACE = schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
VENTILATION_SPACE = schema_enums["VentilationSpaceOptions2019ASHRAE901"]
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
            each_rule=Section19Rule4.RuleSetModelInstanceRule(),
            index_rmr="baseline",
            id="19-4",
            description="For baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity using equipment hourly schedule shall be the same as the most used hourly weekday schedule from the annual simulation.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1 Exception",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0]",
            required_fields={
                "$": ["calendar"],
                "calendar": ["day_of_week_for_january_1"],
            },
            data_items={
                "day_of_week_for_january_1": (
                    "baseline",
                    "calendar/day_of_week_for_january_1",
                ),
            },
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section19Rule4.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section19Rule4.RuleSetModelInstanceRule.BuildingSegmentRule(),
                index_rmr="baseline",
                list_path="buildings[*].building_segments[*]",
                required_fields={
                    "$": ["schedules"],
                },
            )

        def create_data(self, context, data):
            rmi_b = context.baseline
            schedule_b = rmi_b["schedules"]

            return {schedule["id"]: schedule for schedule in schedule_b}

        class BuildingSegmentRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    Section19Rule4.RuleSetModelInstanceRule.BuildingSegmentRule, self
                ).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    each_rule=Section19Rule4.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule(),
                    index_rmr="baseline",
                    list_path="$.zones[*]",
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

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(
                        Section19Rule4.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                        each_rule=Section19Rule4.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule.SpaceRule(),
                        index_rmr="baseline",
                        list_path="$.spaces[*]",
                        required_fields={
                            "$": ["infiltration"],
                        },
                    )

                def create_data(self, context, data):
                    day_of_week_for_january_1 = data["day_of_week_for_january_1"]
                    zone_b = context.baseline

                    # check infiltration
                    inf_pass_cooling = True
                    infiltration_b = zone_b["infiltration"]
                    multiplier_schedule_infiltration = infiltration_b[
                        "multiplier_schedule"
                    ]
                    multiplier_sch = data[multiplier_schedule_infiltration]
                    hourly_values = multiplier_sch["hourly_values"]

                    most_used_weekday_hourly_schedule = (
                        get_most_used_weekday_hourly_schedule(
                            hourly_values, day_of_week_for_january_1
                        )
                    )
                    for x in range(0, int(len(hourly_values) / 24), 24):
                        if (
                            most_used_weekday_hourly_schedule
                            != hourly_values[x : x + 24]
                        ):
                            inf_pass_cooling = False
                            break

                    return {"inf_pass_cooling": inf_pass_cooling}

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(
                            Section19Rule4.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule.SpaceRule,
                            self,
                        ).__init__(
                            rmrs_used=UserBaselineProposedVals(False, True, False),
                            required_fields={
                                "$": ["lighting_space_type", "ventilation_space_type"],
                            },
                        )

                    def is_applicable(self, context, data=None):
                        space_b = context.baseline
                        lighting_space_type_b = space_b["lighting_space_type"]
                        ventilation_space_type = space_b["ventilation_space_type"]

                        return (
                            lighting_space_type_b == LIGHTING_SPACE.DWELLING_UNIT
                            or ventilation_space_type
                            == VENTILATION_SPACE.TRANSIENT_RESIDENTIAL_DWELLING_UNIT
                        )

                    def get_calc_vals(self, context, data=None):
                        day_of_week_for_january_1 = data["day_of_week_for_january_1"]
                        space_b = context.baseline

                        # check the occupancy schedule
                        occupant_multiplier_schedule_b = space_b[
                            "occupant_multiplier_schedule"
                        ]

                        multiplier_sch = data[occupant_multiplier_schedule_b]
                        hourly_values = multiplier_sch["hourly_values"]

                        most_used_weekday_hourly_schedule = (
                            get_most_used_weekday_hourly_schedule(
                                hourly_values, day_of_week_for_january_1
                            )
                        )
                        occ_pass_cooling = True
                        for x in range(0, int(len(hourly_values) / 24), 24):
                            if (
                                most_used_weekday_hourly_schedule
                                != hourly_values[x : x + 24]
                            ):
                                occ_pass_cooling = False
                                break

                        # check the interior lighting
                        interior_lighting_b = space_b["interior_lighting"]

                        multiplier_sch = data[interior_lighting_b]
                        hourly_values = multiplier_sch["hourly_values"]

                        most_used_weekday_hourly_schedule = (
                            get_most_used_weekday_hourly_schedule(
                                hourly_values, day_of_week_for_january_1
                            )
                        )

                        int_lgt_pass_cooling = True
                        for x in range(0, int(len(hourly_values) / 24), 24):
                            if (
                                most_used_weekday_hourly_schedule
                                != hourly_values[x : x + 24]
                            ):
                                int_lgt_pass_cooling = False
                                break

                        # check the misc equipment
                        miscellaneous_equipment_b = space_b["miscellaneous_equipment"]

                        multiplier_sch = data[miscellaneous_equipment_b]
                        hourly_values = multiplier_sch["hourly_values"]

                        most_used_weekday_hourly_schedule = (
                            get_most_used_weekday_hourly_schedule(
                                hourly_values, day_of_week_for_january_1
                            )
                        )

                        misc_pass_cooling = True
                        for x in range(0, int(len(hourly_values) / 24), 24):
                            if (
                                most_used_weekday_hourly_schedule
                                != hourly_values[x : x + 24]
                            ):
                                misc_pass_cooling = False
                                break

                        return {
                            "occ_pass_cooling": occ_pass_cooling,
                            "int_lgt_pass_cooling": int_lgt_pass_cooling,
                            "misc_pass_cooling": misc_pass_cooling,
                        }

                    def manual_check_required(self, context, calc_vals=None, data=None):
                        space_b = context.baseline

                        bldg_area_is_defined = data["bldg_area_is_defined"]
                        building_area_is_MF_dormitory_or_hotel = data[
                            "building_area_is_MF_dormitory_or_hotel"
                        ]

                        space_lighting_or_vent_space_type_is_defined = True
                        if (
                            space_b.get("lighting_space_type") is None
                            and space_b.get("ventilation_space_type") is None
                        ):
                            space_lighting_or_vent_space_type_is_defined = False

                        return not space_lighting_or_vent_space_type_is_defined and (
                            not bldg_area_is_defined
                            or building_area_is_MF_dormitory_or_hotel
                        )

                    def rule_check(self, context, calc_vals=None, data=None):
                        inf_pass_cooling = data["inf_pass_cooling"]
                        occ_pass_cooling = data["occ_pass_cooling"]
                        int_lgt_pass_cooling = data["int_lgt_pass_cooling"]
                        misc_pass_cooling = data["misc_pass_cooling"]

                        return all(
                            [
                                inf_pass_cooling,
                                occ_pass_cooling,
                                int_lgt_pass_cooling,
                                misc_pass_cooling,
                            ]
                        )

                    def get_fail_msg(self, context, calc_vals=None, data=None):
                        inf_pass_cooling = data["inf_pass_cooling"]
                        occ_pass_cooling = data["occ_pass_cooling"]
                        int_lgt_pass_cooling = data["int_lgt_pass_cooling"]
                        misc_pass_cooling = data["misc_pass_cooling"]

                        return all(
                            [
                                inf_pass_cooling,
                                occ_pass_cooling,
                                int_lgt_pass_cooling,
                                misc_pass_cooling,
                            ]
                        )
