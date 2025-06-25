from pydash import curry, every
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
VENTILATION_SPACE = SchemaEnums.schema_enums["VentilationSpaceOptions2019ASHRAE901"]
LIGHTING_BUILDING_AREA = SchemaEnums.schema_enums[
    "LightingBuildingAreaOptions2019ASHRAE901T951TG38"
]

find_schedule = curry(
    lambda schedules, schedule_id, schedule_type: (
        find_exactly_one(f'$[*][?(@.id="{schedule_id}")]', schedules)
    ).get(schedule_type)
)


class PRM9012019Rule60o81(RuleDefinitionListIndexedBase):
    """Rule 23 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule60o81, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule60o81.RMDRule(),
            index_rmd=BASELINE_0,
            id="19-23",
            description="For cooling sizing runs, schedules for internal loads, including those used for "
            "infiltration, occupants, lighting, gas and electricity using equipment, shall be equal to "
            "the highest hourly value used in the annual simulation runs and applied to the entire design "
            "day. For heating sizing runs, schedules for internal loads, including those used for "
            "occupants, lighting, gas and electricity using equipment, shall be equal to the lowest "
            "hourly value used in the annual simulation runs, and schedules for infiltration shall be "
            "equal to the highest hourly value used in the annual simulation runs and applied to the "
            "entire design day.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1 excluding exception",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule60o81.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule60o81.RMDRule.BuildingSegmentRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            schedules_b = getattr_(rmd_b, "rmd", "schedules")

            return {"find_schedule_from_schedules": find_schedule(schedules_b)}

        class BuildingSegmentRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(PRM9012019Rule60o81.RMDRule.BuildingSegmentRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    each_rule=PRM9012019Rule60o81.RMDRule.BuildingSegmentRule.ZoneRule(),
                    index_rmd=BASELINE_0,
                    list_path="$.zones[*]",
                )

            def create_data(self, context, data):
                building_segment_b = context.BASELINE_0

                is_lighting_bldg_area_defined_b = False
                lighting_bldg_type_b = building_segment_b.get(
                    "lighting_building_area_type"
                )

                if lighting_bldg_type_b is not None:
                    is_lighting_bldg_area_defined_b = True

                is_building_area_MF_dormitory_or_hotel_b = lighting_bldg_type_b in [
                    LIGHTING_BUILDING_AREA.DORMITORY,
                    LIGHTING_BUILDING_AREA.HOTEL_MOTEL,
                    LIGHTING_BUILDING_AREA.MULTIFAMILY,
                ]

                return {
                    **data,
                    "is_lighting_bldg_area_defined_b": is_lighting_bldg_area_defined_b,
                    "is_building_area_MF_dormitory_or_hotel_b": is_building_area_MF_dormitory_or_hotel_b,
                }

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(
                        PRM9012019Rule60o81.RMDRule.BuildingSegmentRule.ZoneRule, self
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                        each_rule=PRM9012019Rule60o81.RMDRule.BuildingSegmentRule.ZoneRule.SpaceRule(),
                        index_rmd=BASELINE_0,
                        list_path="$.spaces[*]",
                    )

                def create_data(self, context, data):
                    zone_b = context.BASELINE_0
                    find_schedule_from_schedules = data["find_schedule_from_schedules"]

                    # check infiltration
                    # TODO: need add log here if zone has no infiltration (add TODO lighting, occ, equip)
                    # set default to true in case some zones do not have infiltration
                    # and we do not want to fail those zones.
                    inf_pass_cooling_b = True
                    inf_pass_heating_b = True
                    if zone_b.get("infiltration"):
                        multiplier_sch_inf_id_b = getattr_(
                            zone_b, "Zone", "infiltration", "multiplier_schedule"
                        )
                        multiplier_sch_inf_b = find_schedule_from_schedules(
                            multiplier_sch_inf_id_b
                        )
                        multiplier_sch_hourly_value_b = multiplier_sch_inf_b(
                            "hourly_values"
                        )

                        if (
                            multiplier_sch_inf_b("hourly_heating_design_year")
                            is not None
                        ):
                            design_heating_multiplier_sch_b = multiplier_sch_inf_b(
                                "hourly_heating_design_year"
                            )
                        else:
                            design_heating_multiplier_sch_b = multiplier_sch_inf_b(
                                "hourly_heating_design_day"
                            )

                        if (
                            multiplier_sch_inf_b("hourly_cooling_design_year")
                            is not None
                        ):
                            design_cooling_multiplier_sch_b = multiplier_sch_inf_b(
                                "hourly_cooling_design_year"
                            )
                        else:
                            design_cooling_multiplier_sch_b = multiplier_sch_inf_b(
                                "hourly_cooling_design_day"
                            )

                        max_inf_multiplier_b = max(multiplier_sch_hourly_value_b)
                        inf_pass_cooling_b = every(
                            design_cooling_multiplier_sch_b,
                            lambda multiplier: multiplier == max_inf_multiplier_b
                            or multiplier == -999,
                        )
                        inf_pass_heating_b = every(
                            design_heating_multiplier_sch_b,
                            lambda multiplier: multiplier == max_inf_multiplier_b
                            or multiplier == -999,
                        )

                    return {
                        **data,
                        "inf_pass_cooling_b": inf_pass_cooling_b,
                        "inf_pass_heating_b": inf_pass_heating_b,
                    }

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(
                            PRM9012019Rule60o81.RMDRule.BuildingSegmentRule.ZoneRule.SpaceRule,
                            self,
                        ).__init__(
                            rmds_used=produce_ruleset_model_description(
                                USER=False, BASELINE_0=True, PROPOSED=False
                            ),
                        )

                    def get_calc_vals(self, context, data=None):
                        space_b = context.BASELINE_0
                        find_schedule_from_schedules = data[
                            "find_schedule_from_schedules"
                        ]

                        lighting_space_type_b = space_b.get("lighting_space_type")
                        ventilation_space_type_b = space_b.get("ventilation_space_type")
                        is_space_type_defined_b = bool(
                            lighting_space_type_b or ventilation_space_type_b
                        )
                        is_dwelling_unit_b = (
                            lighting_space_type_b == LIGHTING_SPACE.DWELLING_UNIT
                            or ventilation_space_type_b
                            == VENTILATION_SPACE.TRANSIENT_RESIDENTIAL_DWELLING_UNIT
                        )

                        # check occupancy - set to True as default
                        # do not fail spaces with no schedules
                        occ_pass_cooling_b = True
                        occ_pass_heating_b = True
                        # TODO: need add log here if zone has no infiltration (add TODO lighting, occ, equip)
                        if space_b.get("occupant_multiplier_schedule"):
                            multiplier_sch_occ_b = find_schedule_from_schedules(
                                space_b["occupant_multiplier_schedule"]
                            )
                            multiplier_sch_occ_hourly_value_b = multiplier_sch_occ_b(
                                "hourly_values"
                            )

                            if (
                                multiplier_sch_occ_b("hourly_heating_design_year")
                                is not None
                            ):
                                multiplier_sch_design_heating_occ_b = (
                                    multiplier_sch_occ_b("hourly_heating_design_year")
                                )
                            else:
                                multiplier_sch_design_heating_occ_b = (
                                    multiplier_sch_occ_b("hourly_heating_design_day")
                                )

                            if (
                                multiplier_sch_occ_b("hourly_cooling_design_year")
                                is not None
                            ):
                                multiplier_sch_design_cooling_occ_b = (
                                    multiplier_sch_occ_b("hourly_cooling_design_year")
                                )
                            else:
                                multiplier_sch_design_cooling_occ_b = (
                                    multiplier_sch_occ_b("hourly_cooling_design_day")
                                )

                            max_multiplier_occ = max(multiplier_sch_occ_hourly_value_b)
                            min_multiplier_occ = min(multiplier_sch_occ_hourly_value_b)
                            occ_pass_cooling_b = every(
                                multiplier_sch_design_cooling_occ_b,
                                lambda multiplier: multiplier == max_multiplier_occ
                                or multiplier == -999,
                            )
                            occ_pass_heating_b = every(
                                multiplier_sch_design_heating_occ_b,
                                lambda multiplier: multiplier == min_multiplier_occ
                                or multiplier == -999,
                            )

                        # check interior lighting
                        int_lgt_pass_cooling_b = True
                        int_lgt_pass_heating_b = True
                        for interior_lighting_b in find_all(
                            "$.interior_lighting[*]", space_b
                        ):
                            if int_lgt_pass_cooling_b or int_lgt_pass_heating_b:
                                multiplier_sch_light_id_b = getattr_(
                                    interior_lighting_b,
                                    "Interior Lighting",
                                    "lighting_multiplier_schedule",
                                )

                                multiplier_sch_light_b = find_schedule_from_schedules(
                                    multiplier_sch_light_id_b
                                )
                                multiplier_sch_light_hourly_value_b = (
                                    multiplier_sch_light_b("hourly_values")
                                )

                                if (
                                    multiplier_sch_light_b("hourly_heating_design_year")
                                    is not None
                                ):
                                    multiplier_sch_design_heating_light_b = (
                                        multiplier_sch_light_b(
                                            "hourly_heating_design_year"
                                        )
                                    )
                                else:
                                    multiplier_sch_design_heating_light_b = (
                                        multiplier_sch_light_b(
                                            "hourly_heating_design_day"
                                        )
                                    )

                                if (
                                    multiplier_sch_light_b("hourly_cooling_design_year")
                                    is not None
                                ):
                                    multiplier_sch_design_cooling_light_b = (
                                        multiplier_sch_light_b(
                                            "hourly_cooling_design_year"
                                        )
                                    )

                                else:
                                    multiplier_sch_design_cooling_light_b = (
                                        multiplier_sch_light_b(
                                            "hourly_cooling_design_day"
                                        )
                                    )

                                max_multiplier_light = max(
                                    multiplier_sch_light_hourly_value_b
                                )
                                min_multiplier_light = min(
                                    multiplier_sch_light_hourly_value_b
                                )

                                int_lgt_pass_cooling_b = (
                                    int_lgt_pass_cooling_b
                                    and every(
                                        multiplier_sch_design_cooling_light_b,
                                        lambda x: x == max_multiplier_light
                                        or x == -999,
                                    )
                                )
                                int_lgt_pass_heating_b = (
                                    int_lgt_pass_heating_b
                                    and every(
                                        multiplier_sch_design_heating_light_b,
                                        lambda x: x == min_multiplier_light
                                        or x == -999,
                                    )
                                )

                        # check misc equipment
                        misc_pass_cooling_b = True
                        misc_pass_heating_b = True
                        for misc_equip_b in find_all(
                            "$.miscellaneous_equipment[*]", space_b
                        ):
                            if misc_pass_cooling_b or misc_pass_heating_b:
                                multiplier_sch_misc_b = getattr_(
                                    misc_equip_b,
                                    "Miscellaneous Equipment",
                                    "multiplier_schedule",
                                )
                                multiplier_sch_misc_b = find_schedule_from_schedules(
                                    multiplier_sch_misc_b
                                )
                                multiplier_sch_misc_hourly_value_b = (
                                    multiplier_sch_misc_b("hourly_values")
                                )

                                if (
                                    multiplier_sch_light_b("hourly_heating_design_year")
                                    is not None
                                ):
                                    multiplier_sch_design_heating_misc_b = (
                                        multiplier_sch_misc_b(
                                            "hourly_heating_design_year"
                                        )
                                    )
                                else:
                                    multiplier_sch_design_heating_misc_b = (
                                        multiplier_sch_misc_b(
                                            "hourly_heating_design_day"
                                        )
                                    )

                                if (
                                    multiplier_sch_light_b("hourly_cooling_design_year")
                                    is not None
                                ):
                                    multiplier_sch_design_cooling_misc_b = (
                                        multiplier_sch_misc_b(
                                            "hourly_cooling_design_year"
                                        )
                                    )
                                else:
                                    multiplier_sch_design_cooling_misc_b = (
                                        multiplier_sch_misc_b(
                                            "hourly_cooling_design_day"
                                        )
                                    )

                                max_multiplier_misc = max(
                                    multiplier_sch_misc_hourly_value_b
                                )
                                min_multiplier_misc = min(
                                    multiplier_sch_misc_hourly_value_b
                                )

                                misc_pass_cooling_b = misc_pass_cooling_b and every(
                                    multiplier_sch_design_cooling_misc_b,
                                    lambda x: x == max_multiplier_misc or x == -999,
                                )
                                misc_pass_heating_b = misc_pass_heating_b and every(
                                    multiplier_sch_design_heating_misc_b,
                                    lambda x: x == min_multiplier_misc or x == -999,
                                )

                        return {
                            "is_space_type_defined_b": is_space_type_defined_b,
                            "is_dwelling_unit_b": is_dwelling_unit_b,
                            "is_lighting_bldg_area_defined_b": data[
                                "is_lighting_bldg_area_defined_b"
                            ],
                            "is_building_area_MF_dormitory_or_hotel_b": data[
                                "is_building_area_MF_dormitory_or_hotel_b"
                            ],
                            "inf_pass_cooling_b": data["inf_pass_cooling_b"],
                            "inf_pass_heating_b": data["inf_pass_heating_b"],
                            "occ_pass_cooling_b": occ_pass_cooling_b,
                            "occ_pass_heating_b": occ_pass_heating_b,
                            "int_lgt_pass_cooling_b": int_lgt_pass_cooling_b,
                            "int_lgt_pass_heating_b": int_lgt_pass_heating_b,
                            "misc_pass_cooling_b": misc_pass_cooling_b,
                            "misc_pass_heating_b": misc_pass_heating_b,
                        }

                    def manual_check_required(self, context, calc_vals=None, data=None):
                        is_dwelling_unit_b = calc_vals["is_dwelling_unit_b"]
                        is_space_type_defined_b = calc_vals["is_space_type_defined_b"]
                        is_lighting_bldg_area_defined_b = calc_vals[
                            "is_lighting_bldg_area_defined_b"
                        ]
                        is_heating_schedule_pass = all(
                            [
                                calc_vals["inf_pass_heating_b"],
                                calc_vals["occ_pass_heating_b"],
                                calc_vals["int_lgt_pass_heating_b"],
                                calc_vals["misc_pass_heating_b"],
                            ]
                        )
                        is_cooling_schedule_pass = all(
                            [
                                calc_vals["inf_pass_cooling_b"],
                                calc_vals["occ_pass_cooling_b"],
                                calc_vals["int_lgt_pass_cooling_b"],
                                calc_vals["misc_pass_cooling_b"],
                            ]
                        )

                        # Case 8 exclusion: prevent false undetermined when cooling fails
                        if (
                            not is_dwelling_unit_b
                            and not is_space_type_defined_b
                            and not is_lighting_bldg_area_defined_b
                            and is_heating_schedule_pass
                            and not is_cooling_schedule_pass
                        ):
                            return False

                        return (
                            not is_dwelling_unit_b
                            and not is_space_type_defined_b
                            and is_heating_schedule_pass
                        ) or (is_dwelling_unit_b and is_heating_schedule_pass)

                    def get_manual_check_required_msg(
                        self, context, calc_vals=None, data=None
                    ):
                        space_b = context.BASELINE_0
                        space_id_b = space_b["id"]
                        is_dwelling_unit_b = calc_vals["is_dwelling_unit_b"]
                        is_space_type_defined_b = calc_vals["is_space_type_defined_b"]
                        is_building_area_MF_dormitory_or_hotel_b = calc_vals[
                            "is_building_area_MF_dormitory_or_hotel_b"
                        ]

                        is_heating_schedule_pass = all(
                            [
                                calc_vals["inf_pass_heating_b"],
                                calc_vals["occ_pass_heating_b"],
                                calc_vals["int_lgt_pass_heating_b"],
                                calc_vals["misc_pass_heating_b"],
                            ]
                        )
                        is_cooling_schedule_pass = all(
                            [
                                calc_vals["inf_pass_cooling_b"],
                                calc_vals["occ_pass_cooling_b"],
                                calc_vals["int_lgt_pass_cooling_b"],
                                calc_vals["misc_pass_cooling_b"],
                            ]
                        )

                        if not is_dwelling_unit_b and not is_space_type_defined_b:
                            if is_building_area_MF_dormitory_or_hotel_b:
                                if is_cooling_schedule_pass:
                                    # Case 3
                                    undetermined_msg = (
                                        "The space type was not defined in the RMD and the building area type is multifamily. Heating design schedules were modeled per the rules of G3.1.2.2.1 and PASS; "
                                        "however, cooling design schedules may fall under the exception to Section G3.1.2.2.1 for dwelling units and could not be fully assessed for this check. "
                                        "Conduct manual check to determine if the space is a dwelling unit. If the space is not a dwelling unit then the cooling design schedules pass. "
                                        "If it is a dwelling unit then the cooling design schedules fail this check."
                                    )
                                else:
                                    # Case 4
                                    undetermined_msg = (
                                        "The space type was not defined in the RMD and the building area type is multifamily. Heating design schedules were modeled per the rules of G3.1.2.2.1 and PASS; "
                                        "however, cooling design schedules may fall under the exception to Section G3.1.2.2.1 for dwelling units and could not be fully assessed for this check. "
                                        "Conduct manual check to determine if the space is a dwelling unit. If the space is not a dwelling unit then the cooling design schedules fail. "
                                        "If it is a dwelling unit then conduct a manual check that the schedules meet the requirements under the exception to Section G3.1.2.2.1."
                                    )
                            else:
                                # Case 7
                                undetermined_msg = "Pass unless the space type is dwelling unit. Dwelling units fall under the exception to Section G3.1.2.2.1."
                        elif is_dwelling_unit_b and is_heating_schedule_pass:
                            # Case 6
                            undetermined_msg = (
                                f"{space_id_b} appears to be a dwelling unit and meets the requirements of this rule for heating design schdules. "
                                f"Cooling design schedules fall under the exception to Section G3.1.2.2.1 and were not assessed for this check. "
                                f"Conduct a manual review of cooling design schedules for infiltration, occupants, lighting, gas and electricity using equipment."
                            )

                        return undetermined_msg

                    def rule_check(self, context, calc_vals=None, data=None):
                        is_dwelling_unit_b = calc_vals["is_dwelling_unit_b"]
                        is_space_type_defined_b = calc_vals["is_space_type_defined_b"]
                        is_heating_schedule_pass = all(
                            [
                                calc_vals["inf_pass_heating_b"],
                                calc_vals["occ_pass_heating_b"],
                                calc_vals["int_lgt_pass_heating_b"],
                                calc_vals["misc_pass_heating_b"],
                            ]
                        )
                        is_cooling_schedule_pass = all(
                            [
                                calc_vals["inf_pass_cooling_b"],
                                calc_vals["occ_pass_cooling_b"],
                                calc_vals["int_lgt_pass_cooling_b"],
                                calc_vals["misc_pass_cooling_b"],
                            ]
                        )

                        return (
                            not is_dwelling_unit_b
                            and is_space_type_defined_b
                            and is_heating_schedule_pass
                            and is_cooling_schedule_pass
                        )

                    def get_fail_msg(self, context, calc_vals=None, data=None):
                        space_b = context.BASELINE_0
                        space_id_b = space_b["id"]
                        is_dwelling_unit_b = calc_vals["is_dwelling_unit_b"]
                        is_space_type_defined_b = calc_vals["is_space_type_defined_b"]
                        is_lighting_bldg_area_defined_b = calc_vals[
                            "is_lighting_bldg_area_defined_b"
                        ]
                        is_heating_schedule_pass = all(
                            [
                                calc_vals["inf_pass_heating_b"],
                                calc_vals["occ_pass_heating_b"],
                                calc_vals["int_lgt_pass_heating_b"],
                                calc_vals["misc_pass_heating_b"],
                            ]
                        )
                        is_cooling_schedule_pass = all(
                            [
                                calc_vals["inf_pass_cooling_b"],
                                calc_vals["occ_pass_cooling_b"],
                                calc_vals["int_lgt_pass_cooling_b"],
                                calc_vals["misc_pass_cooling_b"],
                            ]
                        )

                        confirmed_non_dwelling_heat_cool_failed = f"{space_id_b} does not appear to have followed this rule per Section G3.1.2.2.1 for one more more of the following heating or cooling design schedules: infiltration, occupants, lighting, gas and electricity using equipment"
                        deduced_non_dwelling_heat_cool_failed = "The space type nor the building area type were defined in the RMD. The space type was assumed not to be a dwelling unit. Heating design schedules were modeled per the rules of G3.1.2.2.1 and PASS; however, cooling design schedules appear not to meet the requirements of Section G3.1.2.2.1. Fail for the cooling design schedules unless the space type is a dwelling unit. If the space type is a dwelling unit conduct a manual check for the cooling design schedules for compliance with the exception to Section G3.1.2.2.1."
                        dwelling_heat_failed = f"{space_id_b} appears to be a dwelling unit and does not appear to have followed this rule per Section G3.1.2.2.1 for one more more of the following heating design schedules (cooling design schedules fall under the exception to Section G3.1.2.2.1 and were not assessed for dwelling units in this check): infiltration, occupants, lighting, gas and electricity using equipment."

                        failed_msg = ""
                        if is_dwelling_unit_b and not is_heating_schedule_pass:
                            failed_msg = dwelling_heat_failed

                        elif not (is_heating_schedule_pass or is_cooling_schedule_pass):
                            if is_space_type_defined_b:
                                failed_msg = confirmed_non_dwelling_heat_cool_failed
                            elif not is_lighting_bldg_area_defined_b:
                                failed_msg = deduced_non_dwelling_heat_cool_failed

                        elif (
                            not is_dwelling_unit_b
                            and not is_space_type_defined_b
                            and not is_lighting_bldg_area_defined_b
                            and is_heating_schedule_pass
                            and not is_cooling_schedule_pass
                        ):
                            failed_msg = deduced_non_dwelling_heat_cool_failed

                        return failed_msg
