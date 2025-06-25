from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_schedule

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
MANUAL_CHECK_REQUIRED_MSG_CASE_4 = "A reduced schedule and automatic receptacle controls are present in the proposed design. The space type may have receptacle control requirements in Section 8.4.2. If that is the case, there should be no reduced schedule modeled."
MANUAL_CHECK_REQUIRED_MSG_CASE_7 = "The proposed miscellaneous equipment schedule has reduced equivalent full load hours compared the baseline but it could not be determined if automatic receptacle controls are present in the proposed design to justify the credit."
FAIL_MSG_CASE_2 = "The baseline miscellaneous equipment schedule has automatic receptacle controls indicating that there is an applicable requirement for automatic controls for the space in Section 8.4.2. Miscellaneous equipment schedules may only differ when the proposed design has automatic receptacle controls and there are no applicable requirements in Section 8.4.2 for the space."
FAIL_MSG_CASE_6 = "Rule evaluation fails with a conservative outcome. The proposed schedule equivalent full load hours is greater than the baseline."


class PRM9012019Rule66e91(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(PRM9012019Rule66e91, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule66e91.RMDRule(),
            index_rmd=BASELINE_0,
            id="12-2",
            description=(
                "Depending on the space type, receptacle controls may be required by 90.1 Section 8.4.2. Receptacle schedules shall be modeled identically to the proposed design except when receptacle controls are specified in the proposed design for spaces where not required by Section 8.4.2."
            ),
            ruleset_section_title="Receptacle",
            standard_section="Table G3.1-12 Proposed Building Performance column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule66e91.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule66e91.RMDRule.SpaceRule(),
                index_rmd=BASELINE_0,
                list_path="buildings[*].building_segments[*].zones[*].spaces[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            mis_equip_schedule_b_dict = {
                sch_id: find_exactly_one_schedule(rmd_b, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
                    rmd_b,
                )
            }

            mis_equip_schedule_p_dict = {
                sch_id: find_exactly_one_schedule(rmd_p, sch_id)["hourly_values"]
                for sch_id in find_all(
                    "buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
                    rmd_p,
                )
            }
            return {
                "mis_equip_schedule_b_dict": mis_equip_schedule_b_dict,
                "mis_equip_schedule_p_dict": mis_equip_schedule_p_dict,
            }

        class SpaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(PRM9012019Rule66e91.RMDRule.SpaceRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=PRM9012019Rule66e91.RMDRule.SpaceRule.MiscellaneousEquipmentRule(),
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
                        PRM9012019Rule66e91.RMDRule.SpaceRule.MiscellaneousEquipmentRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                    )

                def get_calc_vals(self, context, data=None):
                    misc_equip_b = context.BASELINE_0
                    misc_equip_p = context.PROPOSED

                    space_type_b = data["space_type_b"]
                    mis_equip_schedule_b_dict = data["mis_equip_schedule_b_dict"]
                    mis_equip_schedule_p_dict = data["mis_equip_schedule_p_dict"]
                    misc_equip_schedule_id_b = misc_equip_b.get("multiplier_schedule")
                    misc_equip_schedule_id_p = misc_equip_p.get("multiplier_schedule")

                    misc_equip_schedule_b = mis_equip_schedule_b_dict.get(
                        misc_equip_schedule_id_b
                    )
                    misc_equip_schedule_p = mis_equip_schedule_p_dict.get(
                        misc_equip_schedule_id_p
                    )

                    automatic_controlled_percentage_b = misc_equip_b.get(
                        "automatic_controlled_percentage"
                    )
                    automatic_controlled_percentage_p = misc_equip_p.get(
                        "automatic_controlled_percentage"
                    )
                    auto_receptacle_control_b = (
                        automatic_controlled_percentage_b
                        and automatic_controlled_percentage_b > 0.0
                    )
                    auto_receptacle_control_p = (
                        automatic_controlled_percentage_p
                        and automatic_controlled_percentage_p > 0.0
                    )

                    mask_schedule = [1] * len(misc_equip_schedule_b)
                    schedules_comparison_output = compare_schedules(
                        misc_equip_schedule_b,
                        misc_equip_schedule_p,
                        mask_schedule,
                    )
                    return {
                        # No need to report full schedule values.
                        # "mis_equip_schedule_b_dict": mis_equip_schedule_b_dict,
                        "space_type_b": space_type_b,
                        "auto_receptacle_control_b": auto_receptacle_control_b,
                        "auto_receptacle_control_p": auto_receptacle_control_p,
                        "total_hours_matched": schedules_comparison_output[
                            "total_hours_matched"
                        ],
                        "eflh_difference": schedules_comparison_output[
                            "eflh_difference"
                        ],
                        "hours_misc_equip_schedule_b": len(misc_equip_schedule_b),
                        "hours_misc_equip_schedule_p": len(misc_equip_schedule_p),
                    }

                def manual_check_required(self, context, calc_vals=None, data=None):
                    eflh_difference = calc_vals["eflh_difference"]
                    auto_receptacle_control_b = calc_vals["auto_receptacle_control_b"]
                    auto_receptacle_control_p = calc_vals["auto_receptacle_control_p"]
                    space_type_b = calc_vals["space_type_b"]
                    return (
                        eflh_difference > 0
                        and (
                            auto_receptacle_control_p
                            and space_type_b in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES
                            and not auto_receptacle_control_b
                        )
                        or space_type_b is None
                        or auto_receptacle_control_p is None
                    )

                def get_manual_check_required_msg(
                    self, context, calc_vals=None, data=None
                ):
                    auto_receptacle_control_p = calc_vals["auto_receptacle_control_p"]
                    return (
                        MANUAL_CHECK_REQUIRED_MSG_CASE_7
                        if auto_receptacle_control_p is None
                        else MANUAL_CHECK_REQUIRED_MSG_CASE_4
                    )

                def rule_check(self, context, calc_vals=None, data=None):
                    hours_misc_equip_schedule_b = calc_vals[
                        "hours_misc_equip_schedule_b"
                    ]
                    hours_misc_equip_schedule_p = calc_vals[
                        "hours_misc_equip_schedule_p"
                    ]
                    eflh_difference = calc_vals["eflh_difference"]
                    total_hours_matched = calc_vals["total_hours_matched"]
                    space_type_b = data["space_type_b"]
                    auto_receptacle_control_p = calc_vals["auto_receptacle_control_p"]
                    return (
                        total_hours_matched
                        == hours_misc_equip_schedule_b
                        == hours_misc_equip_schedule_p
                        or eflh_difference > 0
                        and auto_receptacle_control_p
                        and space_type_b not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES
                    )

                def get_fail_msg(self, context, calc_vals=None, data=None):
                    auto_receptacle_control_b = calc_vals["auto_receptacle_control_b"]
                    eflh_difference = calc_vals["eflh_difference"]
                    auto_receptacle_control_p = calc_vals["auto_receptacle_control_p"]
                    if (
                        auto_receptacle_control_p
                        and auto_receptacle_control_b
                        and eflh_difference != 0
                    ):
                        return FAIL_MSG_CASE_2
                    elif eflh_difference < 0:
                        return FAIL_MSG_CASE_6
                    else:
                        return ""
