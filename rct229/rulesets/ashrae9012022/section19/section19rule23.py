from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
VENTILATION_SPACE = SchemaEnums.schema_enums["VentilationSpaceOptions2019ASHRAE901"]
LIGHTING_BUILDING_AREA = SchemaEnums.schema_enums[
    "LightingBuildingAreaOptions2019ASHRAE901T951TG38"
]


def build_schedule_lookup(schedules):
    lookup = {}
    for sch in schedules:
        hourly = sch.get("hourly_values") or []
        lookup[sch["id"]] = {
            "hourly": hourly,
            "max": max(hourly) if hourly else None,
            "min": min(hourly) if hourly else None,
            "cooling": sch.get("hourly_cooling_design_year")
            or sch.get("hourly_cooling_design_day"),
            "heating": sch.get("hourly_heating_design_year")
            or sch.get("hourly_heating_design_day"),
        }
    return lookup


def schedule_all_equal_or_flagged(values, target):
    assert_(values is not None, "Hourly cooling design schedule must exist.")
    for v in values:
        if v != target and v != -999:
            return False
    return True


class PRM9012022Rule60o81(RuleDefinitionListIndexedBase):
    def __init__(self):
        super().__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012022Rule60o81.RMDRule(),
            index_rmd=BASELINE_0,
            id="19-23",
            description="Schedules for internal loads shall match annual extrema on design days.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.2.1 excluding exception",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super().__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012022Rule60o81.RMDRule.BuildingSegmentRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*]",
            )

        def create_data(self, context, data):
            schedules = getattr_(context.BASELINE_0, "rmd", "schedules")
            return {"schedule_lookup": build_schedule_lookup(schedules)}

        class BuildingSegmentRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super().__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    each_rule=PRM9012022Rule60o81.RMDRule.BuildingSegmentRule.ZoneRule(),
                    index_rmd=BASELINE_0,
                    list_path="$.zones[*]",
                )

            def create_data(self, context, data):
                seg = context.BASELINE_0
                bldg_type = seg.get("lighting_building_area_type")
                return {
                    **data,
                    "is_lighting_bldg_area_defined_b": bldg_type is not None,
                    "is_building_area_MF_dormitory_or_hotel_b": bldg_type
                    in {
                        LIGHTING_BUILDING_AREA.DORMITORY,
                        LIGHTING_BUILDING_AREA.HOTEL_MOTEL,
                        LIGHTING_BUILDING_AREA.MULTIFAMILY,
                    },
                }

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super().__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=False
                        ),
                        each_rule=PRM9012022Rule60o81.RMDRule.BuildingSegmentRule.ZoneRule.SpaceRule(),
                        index_rmd=BASELINE_0,
                        list_path="$.spaces[*]",
                    )

                def create_data(self, context, data):
                    zone = context.BASELINE_0
                    lookup = data["schedule_lookup"]

                    inf_pass_cooling = True
                    inf_pass_heating = True

                    inf = zone.get("infiltration")
                    if inf:
                        sch = lookup[inf["multiplier_schedule"]]
                        assert_(sch["hourly"], "Infiltration hourly schedule missing")

                        inf_pass_cooling = schedule_all_equal_or_flagged(
                            sch["cooling"], sch["max"]
                        )
                        inf_pass_heating = schedule_all_equal_or_flagged(
                            sch["heating"], sch["max"]
                        )

                    return {
                        **data,
                        "inf_pass_cooling_b": inf_pass_cooling,
                        "inf_pass_heating_b": inf_pass_heating,
                    }

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super().__init__(
                            rmds_used=produce_ruleset_model_description(
                                USER=False, BASELINE_0=True, PROPOSED=False
                            )
                        )

                    def get_calc_vals(self, context, data=None):
                        space = context.BASELINE_0
                        lookup = data["schedule_lookup"]

                        lighting_type = space.get("lighting_space_type")
                        ventilation_type = space.get("ventilation_space_type")

                        is_space_type_defined = bool(lighting_type or ventilation_type)
                        is_dwelling = (
                            lighting_type == LIGHTING_SPACE.DWELLING_UNIT
                            or ventilation_type
                            == VENTILATION_SPACE.TRANSIENT_RESIDENTIAL_DWELLING_UNIT
                        )

                        def check_schedule(sch_id, is_cooling):
                            if not sch_id:
                                return True
                            sch = lookup[sch_id]
                            hourly = sch["hourly"]
                            assert_(hourly, "Hourly schedule missing")

                            target = sch["max"] if is_cooling else sch["min"]
                            design = sch["cooling"] if is_cooling else sch["heating"]
                            assert_(design, "Design schedule missing")

                            return schedule_all_equal_or_flagged(design, target)

                        occ_cool = check_schedule(
                            space.get("occupant_multiplier_schedule"), True
                        )
                        occ_heat = check_schedule(
                            space.get("occupant_multiplier_schedule"), False
                        )

                        int_lgt_cool = True
                        int_lgt_heat = True
                        for lgt in space.get("interior_lighting", []):
                            sid = lgt.get("lighting_multiplier_schedule")
                            int_lgt_cool &= check_schedule(sid, True)
                            int_lgt_heat &= check_schedule(sid, False)

                        misc_cool = True
                        misc_heat = True
                        for eq in space.get("miscellaneous_equipment", []):
                            sid = eq.get("multiplier_schedule")
                            misc_cool &= check_schedule(sid, True)
                            misc_heat &= check_schedule(sid, False)

                        return {
                            "is_dwelling_unit_b": is_dwelling,
                            "is_space_type_defined_b": is_space_type_defined,
                            "is_lighting_bldg_area_defined_b": data[
                                "is_lighting_bldg_area_defined_b"
                            ],
                            "is_building_area_MF_dormitory_or_hotel_b": data[
                                "is_building_area_MF_dormitory_or_hotel_b"
                            ],
                            "inf_pass_cooling_b": data["inf_pass_cooling_b"],
                            "inf_pass_heating_b": data["inf_pass_heating_b"],
                            "occ_pass_cooling_b": occ_cool,
                            "occ_pass_heating_b": occ_heat,
                            "int_lgt_pass_cooling_b": int_lgt_cool,
                            "int_lgt_pass_heating_b": int_lgt_heat,
                            "misc_pass_cooling_b": misc_cool,
                            "misc_pass_heating_b": misc_heat,
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
