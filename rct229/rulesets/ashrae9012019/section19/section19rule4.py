from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_most_used_weekday_hourly_schedule import (
    get_most_used_weekday_hourly_schedule,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
VENTILATION_SPACE = SchemaEnums.schema_enums["VentilationSpaceOptions2019ASHRAE901"]
LIGHTING_BUILDING_AREA = SchemaEnums.schema_enums[
    "LightingBuildingAreaOptions2019ASHRAE901T951TG38"
]


class PRM9012019Rule74p61(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule74p61, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule74p61.RuleSetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="19-4",
            description="For baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity using equipment hourly schedule shall be the same as the most used hourly weekday schedule from the annual simulation.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1 Exception",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule74p61.RuleSetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule74p61.RuleSetModelInstanceRule.BuildingSegmentRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*]",
                required_fields={
                    "$": ["calendar"],
                    "calendar": ["day_of_week_for_january_1"],
                },
                data_items={
                    "day_of_week_for_january_1": (
                        BASELINE_0,
                        "calendar/day_of_week_for_january_1",
                    ),
                },
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            day_of_week_for_january_1 = rmd_b["calendar"]["day_of_week_for_january_1"]

            return {
                "schedule_b": getattr_(rmd_b, "RMI", "schedules"),
                "day_of_week_for_january_1": day_of_week_for_january_1,
            }

        class BuildingSegmentRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule74p61.RuleSetModelInstanceRule.BuildingSegmentRule,
                    self,
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    each_rule=PRM9012019Rule74p61.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule(),
                    index_rmd=BASELINE_0,
                    list_path="$.zones[*]",
                )

            def create_data(self, context, data):
                building_segment_b = context.BASELINE_0

                is_lighting_bldg_area_defined_b = False
                is_building_area_MF_dormitory_or_hotel_b = False
                lighting_bldg_type_b = building_segment_b.get(
                    "lighting_building_area_type"
                )
                if lighting_bldg_type_b is not None:
                    is_lighting_bldg_area_defined_b = True
                if lighting_bldg_type_b in [
                    LIGHTING_BUILDING_AREA.DORMITORY,
                    LIGHTING_BUILDING_AREA.HOTEL_MOTEL,
                    LIGHTING_BUILDING_AREA.MULTIFAMILY,
                ]:
                    is_building_area_MF_dormitory_or_hotel_b = True

                return {
                    "is_lighting_bldg_area_defined_b": is_lighting_bldg_area_defined_b,
                    "is_building_area_MF_dormitory_or_hotel_b": is_building_area_MF_dormitory_or_hotel_b,
                }

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(
                        PRM9012019Rule74p61.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                        each_rule=PRM9012019Rule74p61.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule.SpaceRule(),
                        index_rmd=BASELINE_0,
                        list_path="$.spaces[*]",
                    )

                def create_data(self, context, data):
                    day_of_week_for_january_1 = data["day_of_week_for_january_1"]
                    schedule_b = data["schedule_b"]
                    zone_b = context.BASELINE_0

                    # check infiltration
                    inf_pass_cooling_b = True
                    # TODO: need add log here if zone has no infiltration (add TODO lighting, occ, equip)
                    if zone_b.get("infiltration"):
                        multiplier_sch_inf_b = getattr_(
                            zone_b, "Zone", "infiltration", "multiplier_schedule"
                        )
                        multiplier_sch_hourly_value_b = getattr_(
                            find_exactly_one_with_field_value(
                                "$[*]",
                                "id",
                                multiplier_sch_inf_b,
                                schedule_b,
                            ),
                            "schedule",
                            "hourly_values",
                        )

                        design_cooling_multiplier_sch_b = getattr_(
                            find_exactly_one_with_field_value(
                                "$[*]",
                                "id",
                                multiplier_sch_inf_b,
                                schedule_b,
                            ),
                            "schedule",
                            "hourly_cooling_design_day",
                        )

                        most_used_weekday_hourly_schedule_b = (
                            get_most_used_weekday_hourly_schedule(
                                multiplier_sch_hourly_value_b, day_of_week_for_january_1
                            )
                        )
                        inf_pass_cooling_b = (
                            design_cooling_multiplier_sch_b
                            == most_used_weekday_hourly_schedule_b
                        )

                    return {"inf_pass_cooling_b": inf_pass_cooling_b}

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(
                            PRM9012019Rule74p61.RuleSetModelInstanceRule.BuildingSegmentRule.ZoneRule.SpaceRule,
                            self,
                        ).__init__(
                            rmds_used=produce_ruleset_model_description(
                                USER=False, BASELINE_0=True, PROPOSED=False
                            ),
                        )

                    def is_applicable(self, context, data=None):
                        space_b = context.BASELINE_0
                        lighting_space_type_b = space_b.get("lighting_space_type")
                        ventilation_space_type_b = space_b.get("ventilation_space_type")

                        return (
                            lighting_space_type_b == LIGHTING_SPACE.DWELLING_UNIT
                            or ventilation_space_type_b
                            == VENTILATION_SPACE.TRANSIENT_RESIDENTIAL_DWELLING_UNIT
                        )

                    def get_calc_vals(self, context, data=None):
                        inf_pass_cooling_b = data["inf_pass_cooling_b"]
                        day_of_week_for_january_1 = data["day_of_week_for_january_1"]
                        schedule_b = data["schedule_b"]
                        space_b = context.BASELINE_0

                        # check occupancy schedule
                        occ_pass_cooling_b = False
                        # TODO: need add log here if zone has no infiltration (add TODO lighting, occ, equip)
                        if space_b.get("occupant_multiplier_schedule"):
                            multiplier_sch_occ_hourly_value_b = getattr_(
                                find_exactly_one_with_field_value(
                                    "$[*]",
                                    "id",
                                    space_b["occupant_multiplier_schedule"],
                                    schedule_b,
                                ),
                                "schedule",
                                "hourly_values",
                            )
                            design_cooling_multiplier_sch_b = getattr_(
                                find_exactly_one_with_field_value(
                                    "$[*]",
                                    "id",
                                    space_b["occupant_multiplier_schedule"],
                                    schedule_b,
                                ),
                                "schedule",
                                "hourly_cooling_design_day",
                            )

                            most_used_weekday_hourly_schedule_b = (
                                get_most_used_weekday_hourly_schedule(
                                    multiplier_sch_occ_hourly_value_b,
                                    day_of_week_for_january_1,
                                )
                            )
                            occ_pass_cooling_b = (
                                most_used_weekday_hourly_schedule_b
                                == design_cooling_multiplier_sch_b
                            )

                        # check interior lighting
                        int_lgt_pass_cooling_b = False
                        for interior_lighting_b in find_all(
                            "$.interior_lighting[*]", space_b
                        ):
                            if not int_lgt_pass_cooling_b:
                                multiplier_sch_light_b = getattr_(
                                    interior_lighting_b,
                                    "Interior Lighting",
                                    "lighting_multiplier_schedule",
                                )

                                multiplier_sch_hourly_value_b = getattr_(
                                    find_exactly_one_with_field_value(
                                        "$[*]",
                                        "id",
                                        multiplier_sch_light_b,
                                        schedule_b,
                                    ),
                                    "schedule",
                                    "hourly_values",
                                )

                                design_cooling_multiplier_sch_b = getattr_(
                                    find_exactly_one_with_field_value(
                                        "$[*]",
                                        "id",
                                        multiplier_sch_light_b,
                                        schedule_b,
                                    ),
                                    "schedule",
                                    "hourly_cooling_design_day",
                                )

                                most_used_weekday_hourly_schedule_b = (
                                    get_most_used_weekday_hourly_schedule(
                                        multiplier_sch_hourly_value_b,
                                        day_of_week_for_january_1,
                                    )
                                )
                                int_lgt_pass_cooling_b = (
                                    design_cooling_multiplier_sch_b
                                    == most_used_weekday_hourly_schedule_b
                                )

                        # check misc equipment
                        misc_pass_cooling_b = False
                        for misc_equip_b in find_all(
                            "$.miscellaneous_equipment[*]", space_b
                        ):
                            if not misc_pass_cooling_b:
                                multiplier_sch_light_b = getattr_(
                                    misc_equip_b,
                                    "miscellaneous_equipment",
                                    "multiplier_schedule",
                                )

                                multiplier_sch_hourly_value_b = getattr_(
                                    find_exactly_one_with_field_value(
                                        "$[*]",
                                        "id",
                                        multiplier_sch_light_b,
                                        schedule_b,
                                    ),
                                    "schedule",
                                    "hourly_values",
                                )

                                design_cooling_multiplier_sch_b = getattr_(
                                    find_exactly_one_with_field_value(
                                        "$[*]",
                                        "id",
                                        multiplier_sch_light_b,
                                        schedule_b,
                                    ),
                                    "schedule",
                                    "hourly_cooling_design_day",
                                )

                                most_used_weekday_hourly_schedule_b = (
                                    get_most_used_weekday_hourly_schedule(
                                        multiplier_sch_hourly_value_b,
                                        day_of_week_for_january_1,
                                    )
                                )
                                misc_pass_cooling_b = (
                                    design_cooling_multiplier_sch_b
                                    == most_used_weekday_hourly_schedule_b
                                )

                        return {
                            "inf_pass_cooling_b": inf_pass_cooling_b,
                            "occ_pass_cooling_b": occ_pass_cooling_b,
                            "int_lgt_pass_cooling_b": int_lgt_pass_cooling_b,
                            "misc_pass_cooling_b": misc_pass_cooling_b,
                        }

                    def manual_check_required(self, context, calc_vals=None, data=None):
                        space_b = context.BASELINE_0

                        is_lighting_bldg_area_defined_b = data[
                            "is_lighting_bldg_area_defined_b"
                        ]
                        is_building_area_MF_dormitory_or_hotel_b = data[
                            "is_building_area_MF_dormitory_or_hotel_b"
                        ]

                        space_lighting_or_vent_space_type_not_defined = (
                            space_b.get("lighting_space_type") is None
                            or space_b.get("ventilation_space_type") is None
                        )

                        return space_lighting_or_vent_space_type_not_defined and (
                            not is_lighting_bldg_area_defined_b
                            or is_building_area_MF_dormitory_or_hotel_b
                        )

                    def get_manual_check_required_msg(
                        self, context, calc_vals=None, data=None
                    ):
                        space_b = context.BASELINE_0
                        space_id_b = space_b["id"]

                        inf_pass_cooling_b = calc_vals["inf_pass_cooling_b"]
                        occ_pass_cooling_b = calc_vals["occ_pass_cooling_b"]
                        int_lgt_pass_cooling_b = calc_vals["int_lgt_pass_cooling_b"]
                        misc_pass_cooling_b = calc_vals["misc_pass_cooling_b"]

                        if all(
                            [
                                inf_pass_cooling_b,
                                occ_pass_cooling_b,
                                int_lgt_pass_cooling_b,
                                misc_pass_cooling_b,
                            ]
                        ):
                            be_verb = "was"
                        else:
                            be_verb = "was not"

                        return f"It is not clear from the RMD if {space_id_b} is a dwelling unit. If it is a dwelling unit it is required that it be modeled following the rule that for baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity design day cooling schedules shalled be modeled using an equipment hourly schedule that is the same as the most used hourly weekday schedule from the annual simulation. This rule {be_verb} followed for this space if applicable."

                    def rule_check(self, context, calc_vals=None, data=None):
                        inf_pass_cooling_b = calc_vals["inf_pass_cooling_b"]
                        occ_pass_cooling_b = calc_vals["occ_pass_cooling_b"]
                        int_lgt_pass_cooling_b = calc_vals["int_lgt_pass_cooling_b"]
                        misc_pass_cooling_b = calc_vals["misc_pass_cooling_b"]

                        return all(
                            [
                                inf_pass_cooling_b,
                                occ_pass_cooling_b,
                                int_lgt_pass_cooling_b,
                                misc_pass_cooling_b,
                            ]
                        )

                    def get_fail_msg(self, context, calc_vals=None, data=None):
                        space_b = context.BASELINE_0
                        space_id_b = space_b["id"]

                        inf_pass_cooling_b = calc_vals["inf_pass_cooling_b"]
                        occ_pass_cooling_b = calc_vals["occ_pass_cooling_b"]
                        int_lgt_pass_cooling_b = calc_vals["int_lgt_pass_cooling_b"]
                        misc_pass_cooling_b = calc_vals["misc_pass_cooling_b"]

                        inf_msg = "" if inf_pass_cooling_b else "infiltration"
                        occ_msg = "" if occ_pass_cooling_b else "occupants"
                        light_msg = "" if int_lgt_pass_cooling_b else "lighting"
                        misc_msg = (
                            ""
                            if misc_pass_cooling_b
                            else "gas and/or electricity miscellaneous"
                        )

                        agg_msg = " ".join(
                            [inf_msg, occ_msg, light_msg, misc_msg]
                        ).replace(" ", ", ")

                        return f"{space_id_b} does not appear to have been modeled following the rule that for baseline cooling sizing runs in residential dwelling units hourly schedules shall be the same as the most used hourly weekday schedule from the annual simulation for the following schedules: {agg_msg}."
