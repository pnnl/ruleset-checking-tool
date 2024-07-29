from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.schema.schema_enums import SchemaEnums

LIGHTING_SPACE_OPTIONS = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]

EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES = [
    LIGHTING_SPACE_OPTIONS.OFFICE_ENCLOSED,
    LIGHTING_SPACE_OPTIONS.CONFERENCE_MEETING_MULTIPURPOSE_ROOM,
    LIGHTING_SPACE_OPTIONS.COPY_PRINT_ROOM,
    LIGHTING_SPACE_OPTIONS.LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY,
    LIGHTING_SPACE_OPTIONS.LOUNGE_BREAKROOM_ALL_OTHERS,
    LIGHTING_SPACE_OPTIONS.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY,
    LIGHTING_SPACE_OPTIONS.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL,
    LIGHTING_SPACE_OPTIONS.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER,
    LIGHTING_SPACE_OPTIONS.OFFICE_OPEN_PLAN,
]
MANUAL_CHECK_REQUIRED_MSG = "A reduced schedule and automatic receptacle controls are present in the proposed design. The space type may have receptacle control requirements in Section 8.4.2. If that is the case, there should be no reduced schedule modeled."


class Section12Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(Section12Rule2, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section12Rule2.SpaceRule(),
            index_rmd=BASELINE_0,
            id="12-2",
            description=(
                "Depending on the space type, receptacle controls may be required by 90.1 Section 8.4.2. Receptacle schedules shall be modeled identically to the proposed design except when receptacle controls are specified in the proposed design for spaces where not required by Section 8.4.2."
            ),
            ruleset_section_title="Receptacle",
            standard_section="Table G3.1-12 Proposed Building Performance column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*].spaces[*]",
            required_fields={"$": ["calendar"], "$.calendar": ["is_leap_year"]},
            data_items={"is_leap_year": (BASELINE_0, "calendar/is_leap_year")},
        )

    class SpaceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section12Rule2.SpaceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section12Rule2.SpaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.miscellaneous_equipment[*]",
            )

        def create_data(self, context, data):
            space_b = context.BASELINE_0
            space_type_b = space_b.get("lighting_space_type")
            return {
                "space_type_b": space_type_b,
            }

        class MiscellaneousEquipmentRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section12Rule2.SpaceRule.MiscellaneousEquipmentRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                )

            def get_calc_vals(self, context, data=None):
                is_leap_year = data["is_leap_year"]
                misc_equip_b = context.BASELINE_0
                misc_equip_p = context.PROPOSED

                misc_equip_schedule_b = misc_equip_b.get("multiplier_schedule")
                misc_equip_schedule_p = misc_equip_p.get("multiplier_schedule")
                auto_receptacle_control_b = misc_equip_b.get("has_automatic_control")
                auto_receptacle_control_p = misc_equip_p.get("has_automatic_control")
                mask_schedule = [1] * 8784 if is_leap_year else [1] * 8760
                comparison_data = compare_schedules(
                    misc_equip_schedule_b,
                    misc_equip_schedule_p,
                    mask_schedule,
                    is_leap_year,
                )
                return {
                    "auto_receptacle_control_b": auto_receptacle_control_b,
                    "auto_receptacle_control_p": auto_receptacle_control_p,
                    "comparison_data": comparison_data,
                    "misc_equip_schedule_b": misc_equip_schedule_b,
                    "misc_equip_schedule_p": misc_equip_schedule_p,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                comparison_data = calc_vals["comparison_data"]
                auto_receptacle_controls_p = calc_vals["auto_receptacle_controls_p"]
                space_type_b = data["space_type_b"]
                return comparison_data["eflh_difference"] > 0 and (
                    auto_receptacle_controls_p
                    and space_type_b in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES
                    or space_type_b is None
                )

            def rule_check(self, context, calc_vals=None, data=None):
                misc_equip_schedule_b = calc_vals["misc_equip_schedule_b"]
                misc_equip_schedule_p = calc_vals["misc_equip_schedule_p"]
                comparison_data = calc_vals["comparison_data"]
                space_type_b = data["space_type_b"]
                auto_receptacle_controls_p = calc_vals["auto_receptacle_controls_p"]
                return (
                    comparison_data["total_hours_matched"]
                    == len(misc_equip_schedule_b)
                    == len(misc_equip_schedule_p)
                    or comparison_data["eflh_difference"] > 0
                    and auto_receptacle_controls_p
                    and space_type_b not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES
                )
