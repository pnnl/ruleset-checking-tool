from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
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
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.compare_standard_val import std_le
from rct229.utils.jsonpath_utils import find_all, find_one
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
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
LABORATORY_TEMP_DELTA = 17.0 * ureg("delta_degF")
GENERAL_TEMP_DELTA = 20.0 * ureg("delta_degF")


class PRM9012019Rule77j17(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule77j17, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule77j17.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-13",
            description="For baseline system types 1-8 and 11-13, system design supply airflow rates shall be based on a supply-air-to-room temperature set-point difference of 20°F or the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater. For systems with multiple zone thermostat setpoints, use the design set point that will result in the lowest supply air cooling set point or highest supply air heating set point.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.8.1 and Exception 1",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            precision={
                "delta_supply_and_design_heating_temp": {
                    "precision": 1,
                    "unit": "delta_degF",
                },
                "delta_supply_and_design_cooling_temp": {
                    "precision": 1,
                    "unit": "delta_degF",
                },
            },
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return any(
            [
                baseline_system_types_dict[system_type]
                and baseline_system_type_compare(
                    system_type, applicable_sys_type, False
                )
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )

        zone_info = {}
        design_thermostat_cooling_setpoint = []
        design_thermostat_heating_setpoint = []
        for hvac_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b:
            zone_info[hvac_id_b] = {
                "are_all_hvac_sys_fan_objs_autosized": are_all_hvac_sys_fan_objs_autosized(
                    rmd_b, hvac_id_b
                ),
                "zone_has_lab_space": False,
                "all_design_setpoints_delta_Ts_are_per_reqs": False,
                "supply_flow_p": ZERO.FLOW,
            }

            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]:
                zone_b = find_one(
                    f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")]',
                    rmd_b,
                )
                design_thermostat_cooling_setpoint.append(
                    getattr_(zone_b, "zones", "design_thermostat_cooling_setpoint")
                )
                design_thermostat_heating_setpoint.append(
                    getattr_(zone_b, "zones", "design_thermostat_heating_setpoint")
                )

                zone_info[hvac_id_b]["zone_has_lab_space"] = any(
                    [
                        space_b.get("lighting_space_type")
                        == LIGHTING_SPACE.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                        for space_b in find_all("$.spaces[*]", zone_b)
                    ]
                )

                for terminal_b in getattr_(zone_b, "zones", "terminals"):
                    if (
                        terminal_b["id"]
                        in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                            hvac_id_b
                        ]["terminal_unit_list"]
                    ):
                        delta_supply_and_design_heating_temp = (
                            getattr_(
                                terminal_b,
                                "terminals",
                                "supply_design_heating_setpoint_temperature",
                            )
                            - design_thermostat_heating_setpoint[-1]
                        )
                        delta_supply_and_design_cooling_temp = (
                            design_thermostat_cooling_setpoint[-1]
                            - getattr_(
                                terminal_b,
                                "terminals",
                                "supply_design_cooling_setpoint_temperature",
                            )
                        )

                        if zone_info[hvac_id_b]["zone_has_lab_space"]:
                            zone_info[hvac_id_b][
                                "all_design_setpoints_delta_Ts_are_per_reqs"
                            ] = all(
                                [
                                    self.precision_comparison[
                                        "delta_supply_and_design_heating_temp"
                                    ](
                                        delta_supply_and_design_heating_temp,
                                        LABORATORY_TEMP_DELTA,
                                    ),
                                    self.precision_comparison[
                                        "delta_supply_and_design_cooling_temp"
                                    ](
                                        delta_supply_and_design_cooling_temp,
                                        LABORATORY_TEMP_DELTA,
                                    ),
                                ]
                            )
                        else:
                            zone_info[hvac_id_b][
                                "all_design_setpoints_delta_Ts_are_per_reqs"
                            ] = all(
                                [
                                    self.precision_comparison[
                                        "delta_supply_and_design_heating_temp"
                                    ](
                                        delta_supply_and_design_heating_temp,
                                        GENERAL_TEMP_DELTA,
                                    ),
                                    self.precision_comparison[
                                        "delta_supply_and_design_cooling_temp"
                                    ](
                                        delta_supply_and_design_cooling_temp,
                                        GENERAL_TEMP_DELTA,
                                    ),
                                ]
                            )

                zone_info[hvac_id_b]["supply_flow_p"] += sum(
                    [
                        terminal_p.get("primary_airflow", ZERO.FLOW)
                        for terminal_p in find_all(
                            f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")].terminals[*]',
                            rmd_p,
                        )
                    ]
                )

            zone_info[hvac_id_b]["design_thermostat_cooling_setpoint"] = min(
                design_thermostat_cooling_setpoint
            )
            zone_info[hvac_id_b]["design_thermostat_heating_setpoint"] = max(
                design_thermostat_heating_setpoint
            )

        return {
            "zone_info": zone_info,
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule77j17.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": ["minimum_outdoor_airflow"],
                },
                precision={
                    "supply_fans_airflow_b": {
                        "precision": 1,
                        "unit": "cfm",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            fan_sys_b = hvac_b["fan_system"]
            hvac_id_b = hvac_b["id"]
            zone_info = data["zone_info"][hvac_id_b]

            all_design_setpoints_delta_Ts_are_per_reqs_b = zone_info[
                "all_design_setpoints_delta_Ts_are_per_reqs"
            ]
            are_all_hvac_sys_fan_objs_autosized_b = zone_info[
                "are_all_hvac_sys_fan_objs_autosized"
            ]

            return {
                "all_design_setpoints_delta_Ts_are_per_reqs_b": all_design_setpoints_delta_Ts_are_per_reqs_b,
                "are_all_hvac_sys_fan_objs_autosized_b": are_all_hvac_sys_fan_objs_autosized_b,
                "fan_minimum_outdoor_airflow_b": CalcQ(
                    "air_flow_rate", fan_sys_b["minimum_outdoor_airflow"]
                ),
                "supply_fans_airflow_b": CalcQ(
                    "air_flow_rate",
                    get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                        fan_sys_b
                    )["supply_fans_airflow"],
                ),
                "supply_airflow_p": CalcQ("air_flow_rate", zone_info["supply_flow_p"]),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            zone_info = data["zone_info"][hvac_id_b]
            supply_fans_airflow_b = calc_vals["supply_fans_airflow_b"]
            all_design_setpoints_delta_Ts_are_per_reqs_b = calc_vals[
                "all_design_setpoints_delta_Ts_are_per_reqs_b"
            ]

            return (
                not all_design_setpoints_delta_Ts_are_per_reqs_b
                and self.precision_comparison["supply_fans_airflow_b"](
                    supply_fans_airflow_b,
                    zone_info["supply_flow_p"],
                )
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
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
                and (
                    self.precision_comparison["supply_fans_airflow_b"](
                        supply_fans_airflow_b, fan_minimum_outdoor_airflow_b
                    )
                    or supply_fans_airflow_b > fan_minimum_outdoor_airflow_b
                )
            ) or (
                (
                    not all_design_setpoints_delta_Ts_are_per_reqs_b
                    and self.precision_comparison["supply_fans_airflow_b"](
                        fan_minimum_outdoor_airflow_b, supply_fans_airflow_b
                    )
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
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
                and std_le(
                    val=supply_fans_airflow_b, std_val=fan_minimum_outdoor_airflow_b
                )
            ) or (
                (
                    not all_design_setpoints_delta_Ts_are_per_reqs_b
                    and std_equal(fan_minimum_outdoor_airflow_b, supply_fans_airflow_b)
                )
            )
