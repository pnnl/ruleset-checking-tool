from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.are_all_hvac_sys_fan_objects_autosized import (
    are_all_hvac_sys_fan_objs_autosized,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_power_flow import (
    get_fan_system_object_supply_return_exhaust_relief_total_power_flow,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]

LIGHTING_SPACE = schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
TEMP_DELTA_17F = 17.0 * ureg("R")
TEMP_DELTA_20F = 20.0 * ureg("R")


class Section19Rule13(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule13, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section19Rule13.HVACRule(),
            index_rmr="baseline",
            id="19-13",
            description="For baseline system types 1-8 and 11-13, system design supply airflow rates shall be based on a supply-air-to-room temperature set-point difference of 20°F or the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater. For systems with multiple zone thermostat setpoints, use the design set point that will result in the lowest supply air cooling set point or highest supply air heating set point.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.8.1 and Exception 1",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        rmi_p = context.proposed

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi_b)
        )

        zone_info = {}
        for hvac_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b:
            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]:
                zone_info[zone_id_b] = {}
                zone_info[zone_id_b][
                    "are_all_hvac_sys_fan_objs_autosized"
                ] = are_all_hvac_sys_fan_objs_autosized(rmi_b, hvac_id_b)
                zone_info[zone_id_b]["supply_airflow_p"] = ZERO.FLOW
                zone_info[zone_id_b][
                    "all_design_setpoints_delta_Ts_are_per_reqs"
                ] = ZERO.TEMPERATURE

                # get `design_thermostat_cooling_setpoint` and `design_thermostat_heating_setpoint`
                for zone_b in find_all(
                    '$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")]',
                    rmi_b,
                ):
                    zone_info[zone_id_b]["design_thermostat_cooling_setpoint"] = min(
                        find_all(
                            f'$.buildings[*].building_segments[*].zones[*][?(@.id == "{zone_id_b}")].design_thermostat_cooling_setpoint',
                            rmi_b,
                        )
                    )
                    zone_info[zone_id_b]["design_thermostat_heating_setpoint"] = max(
                        find_all(
                            f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")].design_thermostat_heating_setpoint',
                            rmi_b,
                        )
                    )

                    for space_b in getattr_(zone_b, "Zone", "spaces"):
                        zone_has_lab_space = (
                            True
                            if (
                                getattr_(space_b, "Space", "lighting_space_type")
                                == LIGHTING_SPACE.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                            )
                            else False
                        )

                    # calculate supply_airflow_p
                    for terminal_p in find_all(
                        '$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")].terminals[*]',
                        rmi_p,
                    ):
                        zone_info[zone_id_b]["supply_airflow_p"] += getattr_(
                            terminal_p, "Terminal", "primary_airflow"
                        )

                for terminal_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                    hvac_id_b
                ]["terminal_unit_list"]:
                    design_heating_supply_air_temp_setpoint = getattr_(
                        terminal_b,
                        "Terminal",
                        "supply_design_heating_setpoint_temperature",
                    )
                    design_cooling_supply_air_temp_setpoint = getattr_(
                        terminal_b,
                        "Terminal",
                        "supply_design_cooling_setpoint_temperature",
                    )

                    if zone_has_lab_space:
                        zone_info[zone_id_b][
                            "all_design_setpoints_delta_Ts_are_per_reqs"
                        ] = (
                            True
                            if (
                                design_heating_supply_air_temp_setpoint
                                - design_cooling_supply_air_temp_setpoint
                            )
                            != TEMP_DELTA_17F
                            else False
                        )

                    else:
                        zone_info[zone_id_b][
                            "all_design_setpoints_delta_Ts_are_per_reqs"
                        ] = (
                            True
                            if (
                                design_heating_supply_air_temp_setpoint
                                - design_cooling_supply_air_temp_setpoint
                            )
                            != TEMP_DELTA_20F
                            else False
                        )

        return {
            "zone_info": zone_info,
        }

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict.keys()
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule13.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": ["minimum_outdoor_airflow"],
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            zone_info = data["zone_info"][hvac_id_b]
            all_design_setpoints_delta_Ts_are_per_reqs_b = zone_info[
                "all_design_setpoints_delta_Ts_are_per_reqs"
            ]
            are_all_hvac_sys_fan_objs_autosized_b = zone_info[
                "are_all_hvac_sys_fan_objs_autosized"
            ]

            fan_sys_b = hvac_b["fan_system"]
            supply_fans_airflow_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )
            fan_minimum_outdoor_airflow_b = fan_sys_b["minimum_outdoor_airflow"]

            supply_airflow_p = zone_info["supply_airflow_p"]

            return {
                "all_design_setpoints_delta_Ts_are_per_reqs_b": all_design_setpoints_delta_Ts_are_per_reqs_b,
                "are_all_hvac_sys_fan_objs_autosized_b": are_all_hvac_sys_fan_objs_autosized_b,
                "supply_fans_airflow_b": CalcQ("air_flow_rate", supply_fans_airflow_b),
                "fan_minimum_outdoor_airflow_b": CalcQ(
                    "air_flow_rate", fan_minimum_outdoor_airflow_b
                ),
                "supply_airflow_p": CalcQ("air_flow_rate", supply_airflow_p),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            zone_info = data["zone_info"][hvac_id_b]
            supply_fans_airflow_b = calc_vals["supply_fans_airflow_b"]

            all_design_setpoints_delta_Ts_are_per_reqs_b = calc_vals[
                "all_design_setpoints_delta_Ts_are_per_reqs_b"
            ]

            return not all_design_setpoints_delta_Ts_are_per_reqs_b and std_equal(
                zone_info["supply_airflow_p"], supply_fans_airflow_b
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            supply_airflow_p = calc_vals["supply_airflow_p"]

            return f"{hvac_id_b} was not modeled based on a supply-air-to-room temperature set-point difference of 20°F (or 17°F, if lab). The baseline and proposed supply airflow was modeled identically at {supply_airflow_p.to('cfm')} CFM. Manual review is required to determine if the airflow rate was modeled to comply with applicable codes or accreditation standards. If not, fail."

        def rule_check(self, context, calc_vals=None, data=None):
            all_design_setpoints_delta_Ts_are_per_reqs_b = calc_vals[
                "all_design_setpoints_delta_Ts_are_per_reqs_b"
            ]
            are_all_hvac_sys_fan_objs_autosized_b = calc_vals[
                "are_all_hvac_sys_fan_objs_autosized_b"
            ]
            supply_fans_airflow_b = calc_vals["supply_fans_airflow_b"]
            fan_minimum_outdoor_airflow_b = calc_vals["fan_minimum_outdoor_airflow_b"]

            return (
                all_design_setpoints_delta_Ts_are_per_reqs_b
                and are_all_hvac_sys_fan_objs_autosized_b
                and supply_fans_airflow_b >= fan_minimum_outdoor_airflow_b
            ) or (
                (
                    not all_design_setpoints_delta_Ts_are_per_reqs_b
                    and std_equal(fan_minimum_outdoor_airflow_b, supply_fans_airflow_b)
                )
            )
