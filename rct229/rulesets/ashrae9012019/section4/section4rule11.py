from pydash import flatten
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
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
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_rmd_dict,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

CONDITIONED_ZONE_TYPE = [
    ZCC.CONDITIONED_MIXED,
    ZCC.CONDITIONED_NON_RESIDENTIAL,
    ZCC.CONDITIONED_RESIDENTIAL,
]

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


class PRM9012019Rule18y74(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 4 (Schedules Setpoints)"""

    def __init__(self):
        super(PRM9012019Rule18y74, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule18y74.RuleSetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="4-11",
            description="Fan schedules shall be modeled identically in the baseline and proposed unless Table G3.1 Section 4 baseline exceptions are applicable. Fan Schedules may be allowed to differ when Section 4 Baseline Column Exceptions #1, #2 Or #3 are applicable.",
            ruleset_section_title="Schedules Setpoints",
            standard_section="Section G3.1-4 Schedule Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="$.ruleset_model_descriptions[0]",
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule18y74.RuleSetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule18y74.RuleSetModelInstanceRule.ZoneRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].zones[*]",
                required_fields={
                    "$": ["weather"],
                    "weather": ["climate_zone"],
                },
            )

        def create_data(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone = rmd_b["weather"]["climate_zone"]

            zone_p_hvac_list_dict = {
                zone_id: get_list_hvac_systems_associated_with_zone(rmd_p, zone_id)
                for zone_id in find_all(
                    "$.buildings[*].building_segments[*].zones[*].id", rmd_p
                )
            }

            zone_p_fan_schedule_dict = {
                zone_id: get_aggregated_zone_hvac_fan_operating_schedule(rmd_p, zone_id)
                for zone_id in find_all(
                    "$.buildings[*].building_segments[*].zones[*].id", rmd_p
                )
            }

            zone_b_hvac_zone_list_dict = {
                hvac_id: find_all(
                    f'$.buildings[*].building_segments[*].zones[*][?(@.terminals[*].served_by_heating_ventilating_air_conditioning_system = "{hvac_id}")].id',
                    rmd_b,
                )
                for hvac_id in find_all(
                    "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
                    rmd_b,
                )
            }

            zone_b_fan_schedule_dict = {
                zone_id: get_aggregated_zone_hvac_fan_operating_schedule(rmd_b, zone_id)
                for zone_id in find_all(
                    "$.buildings[*].building_segments[*].zones[*].id", rmd_b
                )
            }

            floor_b_hvac_list_dict = {
                floor_name: get_dict_of_zones_hvac_sys_serving_specific_floor(
                    rmd_b, floor_name
                )
                for floor_name in find_all(
                    "$.buildings[*].building_segments[*].zones[*].floor_name", rmd_b
                )
            }

            return {
                "climate_zone": climate_zone,
                "baseline_hvac_sys_type_ids_dict_b": get_baseline_system_types(rmd_b),
                "zone_p_hvac_list_dict": zone_p_hvac_list_dict,
                "zone_b_hvac_zone_list_dict": zone_b_hvac_zone_list_dict,
                "zone_p_fan_schedule_dict": zone_p_fan_schedule_dict,
                "zone_b_fan_schedule_dict": zone_b_fan_schedule_dict,
                "floor_b_hvac_list_dict": floor_b_hvac_list_dict,
                "dict_hvac_sys_zones_served_p": get_hvac_zone_list_w_area_by_rmd_dict(
                    rmd_p
                ),
                "zcc_dict_b": get_zone_conditioning_category_rmd_dict(
                    climate_zone, rmd_b
                ),
            }

        def list_filter(self, context_item, data=None):
            zcc_dict_b = data["zcc_dict_b"]
            zone_b = context_item.BASELINE_0
            return zcc_dict_b[zone_b["id"]] in CONDITIONED_ZONE_TYPE

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule18y74.RuleSetModelInstanceRule.ZoneRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["terminals", "floor_name"],
                        "terminal": [
                            "served_by_heating_ventilating_air_conditioning_system"
                        ],
                    },
                )

            def get_calc_vals(self, context, data=None):
                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                zone_p_hvac_list_dict = data["zone_p_hvac_list_dict"]
                zone_p_fan_schedule_dict = data["zone_p_fan_schedule_dict"]
                zone_b_fan_schedule_dict = data["zone_b_fan_schedule_dict"]
                floor_b_hvac_list_dict = data["floor_b_hvac_list_dict"]
                zone_b_hvac_zone_list_dict = data["zone_b_hvac_zone_list_dict"]

                baseline_hvac_sys_type_ids_dict_b = data[
                    "baseline_hvac_sys_type_ids_dict_b"
                ]
                dict_hvac_sys_zones_served_p = data["dict_hvac_sys_zones_served_p"]

                fan_schedule_hourly_values_b = zone_b_fan_schedule_dict[zone_b["id"]]
                fan_schedule_hourly_values_p = zone_p_fan_schedule_dict[zone_p["id"]]

                schedule_mismatch = (
                    fan_schedule_hourly_values_b != fan_schedule_hourly_values_p
                )
                proposed_served_by_multizone = False
                assert_(
                    len(zone_b["terminals"]) == 1,
                    f"Zone {zone_b['id']} has either no HVAC system or more than one HVAC systems which is incorrect in the baseline",
                )
                hvac_id_b = zone_b["terminals"][0][
                    "served_by_heating_ventilating_air_conditioning_system"
                ]

                for sys_type, sys_list in baseline_hvac_sys_type_ids_dict_b.items():
                    if hvac_id_b in baseline_hvac_sys_type_ids_dict_b[sys_type]:
                        hvac_sys_type_b = sys_type

                # Check if the system type is an applicable system type and serves multiple zones
                baseline_served_by_multizone = (
                    hvac_sys_type_b in APPLICABLE_SYS_TYPES
                    and len(next(iter(zone_b_hvac_zone_list_dict.values()))) > 1
                )
                list_hvac_systems_p = zone_p_hvac_list_dict[zone_p["id"]]

                for hvac_id_p in list_hvac_systems_p:
                    if len(dict_hvac_sys_zones_served_p[hvac_id_p]["zone_list"]) > 1:
                        for terminal_p in zone_p["terminals"]:
                            if (
                                terminal_p[
                                    "served_by_heating_ventilating_air_conditioning_system"
                                ]
                                == hvac_id_p
                            ) and terminal_p.get(
                                "heating_capacity", ZERO.POWER
                            ) > ZERO.POWER:
                                proposed_served_by_multizone = True

                system_type_match_baseline_proposed = (
                    proposed_served_by_multizone == baseline_served_by_multizone
                )
                floor_name_b = zone_b["floor_name"]
                dict_of_zones_hvac_systems_serving_specific_floor_b = (
                    floor_b_hvac_list_dict[floor_name_b]
                )
                list_hvac_sys_serving_floor_b = list(
                    set(
                        flatten(
                            (
                                dict_of_zones_hvac_systems_serving_specific_floor_b.values()
                            )
                        )
                    )
                )

                hvac_type_check = False
                for hvac_flr_b in list_hvac_sys_serving_floor_b:
                    for sys_type, sys_list in baseline_hvac_sys_type_ids_dict_b.items():
                        if (
                            hvac_flr_b in baseline_hvac_sys_type_ids_dict_b[sys_type]
                            and sys_type in APPLICABLE_SYS_TYPES
                        ):
                            hvac_type_check = True

                return {
                    "schedule_mismatch": schedule_mismatch,
                    "baseline_served_by_multizone": baseline_served_by_multizone,
                    "proposed_served_by_multizone": proposed_served_by_multizone,
                    "system_type_match_baseline_proposed": system_type_match_baseline_proposed,
                    "hvac_type_check": hvac_type_check,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                system_type_match_baseline_proposed = calc_vals[
                    "system_type_match_baseline_proposed"
                ]

                return not system_type_match_baseline_proposed

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                schedule_mismatch = calc_vals["schedule_mismatch"]
                baseline_served_by_multizone = calc_vals["baseline_served_by_multizone"]
                proposed_served_by_multizone = calc_vals["proposed_served_by_multizone"]
                hvac_type_check = calc_vals["hvac_type_check"]

                if (
                    schedule_mismatch
                    and not baseline_served_by_multizone
                    and hvac_type_check
                    and proposed_served_by_multizone
                ):
                    return (
                        "There is a fan operating schedule mismatch between the baseline and proposed but section g3.1.1(c) appears applicable. "
                        "Verify mismatch is appropriate per section G3.1.1(c) and that the fan operating schedule in the baseline is in alignment with the occupancy schedules."
                    )
                else:
                    return (
                        "Fan schedules match between the baseline and proposed for the hvac system(s) serving this zone. "
                        "Verify that matching schedules are appropriate in that none of the section 4 baseline column exceptions #1, #2 or #3 are applicable."
                    )

            def rule_check(self, context, calc_vals=None, data=None):
                schedule_mismatch = calc_vals["schedule_mismatch"]
                system_type_match_baseline_proposed = calc_vals[
                    "system_type_match_baseline_proposed"
                ]

                return not schedule_mismatch and system_type_match_baseline_proposed

            def get_fail_msg(self, context, calc_vals=None, data=None):

                return (
                    "There is a fan schedule mismatch between the baseline and proposed RMDs for the hvac system(s) serving this zone. "
                    "Fail unless table G3.1 section 4 baseline column exceptions #1, #2 or #3 is applicable."
                )
