from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import PROPOSED
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

MSG_WARN_NA_LTG_POWER = "The zone contains a not-applicable space type with lighting power. Verify that the mandatory daylighting control requirements are met, if applicable."
MSG_WARN_DAYLIGHT_NO_SCHEDULE = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled explicitly in the simulation tool. Verify that the mandatory lighting control requirements are met."
MSG_WARN_DAYLIGHT = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled via schedule adjustment. Verify that the mandatory lighting control requirements are met, and that the supporting documentation is provided for the schedule adjustment."
MSG_WARN_NO_DAYLIGHT = "Some of the spaces in zone are modeled with fenestration but no daylighting controls. The design must include mandatory daylighting controls unless any of the exceptions to 90.1 section 9.4.1.1 apply."

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
EXTERIOR = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"].EXTERIOR
NONE = SchemaEnums.schema_enums["LightingDaylightingControlOptions"].NONE
LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]

NOT_APPLICABLE_SPACE_TYPES = [
    LIGHTING_SPACE.DORMITORY_LIVING_QUARTERS,
    LIGHTING_SPACE.FIRE_STATION_SLEEPING_QUARTERS,
    LIGHTING_SPACE.HEALTHCARE_FACILITY_OPERATING_ROOM,
    # LIGHTING_SPACE.OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS,
    LIGHTING_SPACE.DWELLING_UNIT,
    LIGHTING_SPACE.GUEST_ROOM,
    LIGHTING_SPACE.STORAGE_ROOM_SMALL,
    LIGHTING_SPACE.PARKING_AREA_INTERIOR,
    LIGHTING_SPACE.NONE,
]


class PRM9012022Rule66m62(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2022 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012022Rule66m62, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012022Rule66m62.ZoneRule(),
            index_rmd=PROPOSED,
            id="6-7",
            description="Proposed building is modeled with daylighting controls directly or through schedule adjustments.",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*]",
        )

    class ZoneRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule66m62.ZoneRule, self).__init__(
                required_fields={"$": ["spaces", "surfaces"]},
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
            )

        def get_calc_vals(self, context, data=None):
            zone_p = context.PROPOSED

            daylight_flag_p = (
                len(
                    find_all(
                        # Doors in a surface adjacent to exterior
                        f'$.surfaces[*][?(@.adjacent_to = "{EXTERIOR}")].subsurfaces[*][?(@.classification != "{DOOR}")]',
                        zone_p,
                    )
                )
                > 0
            )

            has_daylight_control_flag_p = (
                len(
                    find_all(
                        # interior_lighting instances with daylighting_control_type set to NONE
                        f'$.spaces[*].interior_lighting[*][?(@.daylighting_control_type!= "{NONE}")]',
                        zone_p,
                    )
                )
                > 0
            )

            daylight_schedule_adjustment_flag_p = any(
                find_all(
                    # interior_lighting instances with are_schedules_used_for_modeling_daylighting_control set to True
                    "$.spaces[*].interior_lighting[*][?(@.are_schedules_used_for_modeling_daylighting_control = true)]",
                    zone_p,
                )
            )

            na_space_with_lighting_power_flag_P = any(
                [
                    space_p.get("lighting_space_type") in NOT_APPLICABLE_SPACE_TYPES
                    and sum(
                        [
                            int_ltg_p.get("power_per_area", 0 * ureg("W/m2"))
                            for int_ltg_p in find_all("$.interior_lighting[*]", space_p)
                        ]
                    )
                    for space_p in find_all("$.spaces[*]", zone_p)
                ]
            )

            return {
                "daylight_flag_p": daylight_flag_p,
                "has_daylight_control_flag_p": has_daylight_control_flag_p,
                "daylight_schedule_adjustment_flag_p": daylight_schedule_adjustment_flag_p,
                "na_space_with_lighting_power_flag_P": na_space_with_lighting_power_flag_P,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            na_space_with_lighting_power_flag_P = calc_vals[
                "na_space_with_lighting_power_flag_P"
            ]
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag_p = calc_vals["has_daylight_control_flag_p"]

            return na_space_with_lighting_power_flag_P or (
                daylight_flag_p and has_daylight_control_flag_p
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            na_space_with_lighting_power_flag_P = calc_vals[
                "na_space_with_lighting_power_flag_P"
            ]
            daylight_schedule_adjustment_flag_p = calc_vals[
                "daylight_schedule_adjustment_flag_p"
            ]

            if na_space_with_lighting_power_flag_P:
                UNDETERMINED_MSG = MSG_WARN_NA_LTG_POWER
            elif daylight_schedule_adjustment_flag_p:
                UNDETERMINED_MSG = MSG_WARN_DAYLIGHT
            elif not daylight_schedule_adjustment_flag_p:
                UNDETERMINED_MSG = MSG_WARN_DAYLIGHT_NO_SCHEDULE

            return UNDETERMINED_MSG

        def rule_check(self, context, calc_vals, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag_p = calc_vals["has_daylight_control_flag_p"]

            return not daylight_flag_p and not has_daylight_control_flag_p

        def get_fail_msg(self, context, calc_vals=None, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag_p = calc_vals["has_daylight_control_flag_p"]

            return (
                MSG_WARN_NO_DAYLIGHT
                if daylight_flag_p and not has_daylight_control_flag_p
                else ""
            )
