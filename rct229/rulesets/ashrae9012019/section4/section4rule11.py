from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_aggregated_zone_hvac_fan_operating_schedule import (
    get_aggregated_zone_hvac_fan_operating_schedule,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_hvac_sys_serving_specific_floor import (
    get_dict_of_zones_hvac_sys_serving_specific_floor,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_7C,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_8A,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_8C,
]


class Section4Rule11(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 4 (Airside System)"""

    def __init__(self):
        super(Section4Rule11, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "calendar": ["is_leap_year"],
            },
            each_rule=Section4Rule11.RuleSetModelInstanceRule(),
            index_rmr=BASELINE_0,
            id="4-11",
            description="Fan schedules shall be modeled identically in the baseline and proposed unless Table G3.1 Section 4 baseline exceptions are applicable. Fan Schedules may be allowed to differ when Section 4 Baseline Column Exceptions #1, #2 Or #3 are applicable.",
            ruleset_section_title="Airside System",
            standard_section="Section G3.1-4 Schedule Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            data_items={"is_leap_year_b": (BASELINE_0, "calendar/is_leap_year")},
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section4Rule11.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section4Rule11.RuleSetModelInstanceRule.ZoneRule(),
                index_rmr=BASELINE_0,
                list_path="$.buildings[*].zones[*]",
            )

        def create_data(self, context, data=None):
            rmi_b = context.BASELINE_0
            rmi_p = context.PROPOSED
            return {
                "rmi_b": rmi_b,
                "rmi_p": rmi_p,
                "baseline_hvac_sys_type_ids_dict_b": get_baseline_system_types(rmi_b),
                "dict_hvac_sys_zones_served_p": get_hvac_zone_list_w_area_dict(rmi_p),
            }

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(Section4Rule11.RuleSetModelInstanceRule.ZoneRule, self,).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["terminals"],
                        "terminal": [
                            "served_by_heating_ventilating_air_conditioning_system"
                        ],
                    },
                )

            def get_calc_vals(self, context, data=None):
                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                is_leap_year = data["is_leap_year"]
                baseline_hvac_sys_type_ids_dict_b = data[
                    "baseline_hvac_sys_type_ids_dict_b"
                ]
                dict_hvac_sys_zones_served_p = data["dict_hvac_sys_zones_served_p"]
                rmi_b = data["rmi_b"]
                rmi_p = data["rmi_p"]

                fan_schedule_b = get_aggregated_zone_hvac_fan_operating_schedule(
                    rmi_b, zone_b["id"], is_leap_year
                )
                fan_schedule_p = get_aggregated_zone_hvac_fan_operating_schedule(
                    rmi_p, zone_p["id"], is_leap_year
                )

                fan_schedule_hourly_values_b = fan_schedule_b.get("hourly_values")
                fan_schedule_hourly_values_p = fan_schedule_p.get("hourly_values")

                schedule_match = (
                    fan_schedule_hourly_values_b == fan_schedule_hourly_values_p
                )

                proposed_served_by_multizone = False
                hvac_id_b = zone_b["terminals"][0][
                    "served_by_heating_ventilating_air_conditioning_system"
                ]
                hvac_sys_type_b = baseline_hvac_sys_type_ids_dict_b.keys()[
                    list(baseline_hvac_sys_type_ids_dict_b.values()).index(hvac_id_b)
                ]

                baseline_served_by_multizone = hvac_sys_type_b in APPLICABLE_SYS_TYPES

                list_hvac_systems_p = get_list_hvac_systems_associated_with_zone(
                    rmi_p, zone_p["id"]
                )
                for hvac_id_p in list_hvac_systems_p:
                    if (
                        len(
                            list(
                                dict_hvac_sys_zones_served_p[hvac_id_p][
                                    "Zone_List"
                                ].values()
                            )
                        )
                        > 1
                    ):
                        for terminal_p in zone_p["terminals"]:
                            if (
                                terminal_p[
                                    "served_by_heating_ventilating_air_conditioning_system"
                                ]
                                == hvac_id_p
                            ):
                                if terminal_p["heating_capacity"] > 0:
                                    proposed_served_by_multizone = True

                system_type_match_baseline_proposed = (
                    proposed_served_by_multizone == baseline_served_by_multizone
                )

                floor_name_b = zone_b["floor_name"]
                dict_of_zones_hvac_systems_serving_specific_floor_b = (
                    get_dict_of_zones_hvac_sys_serving_specific_floor(
                        floor_name_b, rmi_b
                    )
                )

                list_hvac_sys_serving_floor_b = list(
                    dict_of_zones_hvac_systems_serving_specific_floor_b.values()
                )
                hvac_type_check = False
                for hvac_flr_b in list_hvac_sys_serving_floor_b:
                    if (
                        baseline_hvac_sys_type_ids_dict_b.keys()[
                            list(baseline_hvac_sys_type_ids_dict_b.values()).index(
                                hvac_flr_b
                            )
                        ]
                        in APPLICABLE_SYS_TYPES
                    ):
                        hvac_type_check = True

                return {
                    "schedule_match": schedule_match,
                    "baseline_served_by_multizone": baseline_served_by_multizone,
                    "proposed_served_by_multizone": proposed_served_by_multizone,
                    "system_type_match_baseline_proposed": system_type_match_baseline_proposed,
                    "hvac_type_check": hvac_type_check,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                schedule_match = calc_vals["schedule_match"]
                system_type_match_baseline_proposed = calc_vals[
                    "system_type_match_baseline_proposed"
                ]
                return not (schedule_match and system_type_match_baseline_proposed)

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                schedule_match = calc_vals["schedule_match"]
                baseline_served_by_multizone = calc_vals["baseline_served_by_multizone"]
                proposed_served_by_multizone = calc_vals["proposed_served_by_multizone"]
                hvac_type_check = calc_vals["hvac_type_check"]
                if (
                    not schedule_match
                    and not baseline_served_by_multizone
                    and hvac_type_check
                    and proposed_served_by_multizone
                ):
                    return "There is a fan operating schedule mismatch between the baseline and proposed but section g3.1.1(c) appears applicable. Verify mismatch is appropriate per section G3.1.1(c) and that the fan operating schedule in the baseline is in alignment with the occupancy schedules."
                elif not schedule_match:
                    return "There is a fan schedule mismatch between the baseline and proposed rmrs for the hvac system(s) serving this zone. Fail unless table G3.1 section 4 baseline column exceptions #1, #2 or #3 is applicable."
                else:
                    return "Fan schedules match between the baseline and proposed rmrs for the hvac system(s) serving this zone. Verify that matching schedules are appropriate in that none of the section 4 baseline column exceptions #1, #2 or #3 are applicable."

            def rule_check(self, context, calc_vals=None, data=None):
                return True
