from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

MSG_WARN_NA_SPACE_WITH_LIGHTING = "The zone contains a not-applicable space type with lighting power. Verify that the mandatory daylighting control requirements are met, if applicable."
MSG_WARN_DAYLIGHT_NO_SCHEDULE = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled explicitly in the simulation tool. Verify that the mandatory lighting control requirements are met."
MSG_WARN_DAYLIGHT = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled via schedule adjustment. Verify that the mandatory lighting control requirements are met, and that the supporting documentation is provided for the schedule adjustment."
MSG_WARN_NO_DAYLIGHT = "Some of the spaces in zone are modeled with fenestration but no daylighting controls. The design must include mandatory daylighting controls unless any of the exceptions to 90.1 section 9.4.1.1 apply."

VentilationSpaceOptions = SchemaEnums.schema_enums[
    "VentilationSpaceOptions2019ASHRAE901"
]
LightingSpaceOptions = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
EXTERIOR = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"].EXTERIOR
NONE = SchemaEnums.schema_enums["LightingDaylightingControlOptions"].NONE


class PRM9012019Rule66m62(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule66m62, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule66m62.ZoneRule(),
            index_rmd=PROPOSED,
            id="6-7",
            description="Proposed building is modeled with daylighting controls directly or through schedule adjustments.",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*]",
        )

    def list_filter(self, context_item, data):
        zone_p = context_item.PROPOSED

        not_applicable_space_types = {
            LightingSpaceOptions.DORMITORY_LIVING_QUARTERS,
            LightingSpaceOptions.FIRE_STATION_SLEEPING_QUARTERS,
            LightingSpaceOptions.HEALTHCARE_FACILITY_OPERATING_ROOM,
            VentilationSpaceOptions.OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS,
            LightingSpaceOptions.DWELLING_UNIT,
            LightingSpaceOptions.GUEST_ROOM,
            LightingSpaceOptions.STORAGE_ROOM_SMALL,
            LightingSpaceOptions.PARKING_AREA_INTERIOR,
            LightingSpaceOptions.NONE,
        }

        spaces = zone_p.get("spaces", [])

        na_space_with_lighting_power = any(
            (
                space.get("lighting_space_type") in not_applicable_space_types
                or space.get("ventilation_space_type") in not_applicable_space_types
            )
            and sum(
                il.get("power_per_area", 0) for il in space.get("interior_lighting", [])
            )
            > 0
            for space in spaces
        )

        # Skip only if all spaces are not applicable and none have lighting power
        return not (
            all(
                space.get("lighting_space_type") in not_applicable_space_types
                for space in spaces
            )
            and not na_space_with_lighting_power
        )

    class ZoneRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule66m62.ZoneRule, self).__init__(
                required_fields={"$": ["spaces", "surfaces"]},
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
            )

        def get_calc_vals(self, context, data=None):
            zone_p = context.PROPOSED

            not_applicable_space_types = {
                LightingSpaceOptions.DORMITORY_LIVING_QUARTERS,
                LightingSpaceOptions.FIRE_STATION_SLEEPING_QUARTERS,
                LightingSpaceOptions.HEALTHCARE_FACILITY_OPERATING_ROOM,
                VentilationSpaceOptions.OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS,
                LightingSpaceOptions.DWELLING_UNIT,
                LightingSpaceOptions.GUEST_ROOM,
                LightingSpaceOptions.STORAGE_ROOM_SMALL,
                LightingSpaceOptions.PARKING_AREA_INTERIOR,
                LightingSpaceOptions.NONE,
            }

            has_na_space_with_lighting_power = any(
                (
                    space.get("lighting_space_type") in not_applicable_space_types
                    or space.get("ventilation_space_type") in not_applicable_space_types
                )
                and sum(
                    il.get("power_per_area", 0)
                    for il in space.get("interior_lighting", [])
                )
                > 0
                for space in zone_p.get("spaces", [])
            )

            is_daylighting_control_expected = (
                len(
                    find_all(
                        f'$.surfaces[*][?(@.adjacent_to = "{EXTERIOR}")].'
                        f'subsurfaces[*][?(@.classification != "{DOOR}")]',
                        zone_p,
                    )
                )
                > 0
            )

            is_daylighting_control_modeled = (
                len(
                    find_all(
                        f"$.spaces[*].interior_lighting[*]"
                        f'[?(@.daylighting_control_type != "{NONE}")]',
                        zone_p,
                    )
                )
                > 0
            )

            are_schedules_used_for_modeling_daylighting_controls = (
                len(
                    find_all(
                        "$.spaces[*].interior_lighting[*]"
                        "[?(@.are_schedules_used_for_modeling_daylighting_control = true)]",
                        zone_p,
                    )
                )
                > 0
            )

            return {
                "na_space_with_lighting_power": has_na_space_with_lighting_power,
                "is_daylighting_control_expected": is_daylighting_control_expected,
                "is_daylighting_control_modeled": is_daylighting_control_modeled,
                "are_schedules_used_for_modeling_daylighting_controls": (
                    are_schedules_used_for_modeling_daylighting_controls
                ),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            return calc_vals["na_space_with_lighting_power"] or (
                calc_vals["is_daylighting_control_expected"]
                and calc_vals["is_daylighting_control_modeled"]
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            if calc_vals["na_space_with_lighting_power"]:
                return MSG_WARN_NA_SPACE_WITH_LIGHTING

            return (
                MSG_WARN_DAYLIGHT
                if calc_vals["are_schedules_used_for_modeling_daylighting_controls"]
                else MSG_WARN_DAYLIGHT_NO_SCHEDULE
            )

        def rule_check(self, context, calc_vals=None, data=None):
            is_daylighting_control_expected = calc_vals[
                "is_daylighting_control_expected"
            ]
            is_daylighting_control_modeled = calc_vals["is_daylighting_control_modeled"]

            return (
                not is_daylighting_control_expected
                and not is_daylighting_control_modeled
            )

        def get_fail_msg(self, context, calc_vals=None, data=None):
            is_daylighting_control_expected = calc_vals[
                "is_daylighting_control_expected"
            ]
            is_daylighting_control_modeled = calc_vals["is_daylighting_control_modeled"]

            return (
                MSG_WARN_NO_DAYLIGHT
                if is_daylighting_control_expected
                and not is_daylighting_control_modeled
                else ""
            )
