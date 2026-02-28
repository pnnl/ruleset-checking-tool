from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.schedule_utils import get_schedule_year_length

TERMINAL_TYPE = SchemaEnums.schema_enums["TerminalOptions"]
APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
]

VENT_THRESHOLD_FACTOR = 0.5


class PRM9012022Rule46w18(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2022 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012022Rule46w18, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012022Rule46w18.HVACRule(),
            index_rmd=BASELINE_0,
            id="23-9",
            description="System 11 Minimum volume setpoint shall be the largest of 50% of the maximum design airflow rate, the minimum ventilation airflow rate or the airflow required to comply with codes or accredidation standards.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Exception to G3.1.3.13",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
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

        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]
        dict_of_zones_and_terminal_units_served_by_hvac_sys = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )
        zones_p = find_all("$.buildings[*].building_segments[*].zones[*]", rmd_p)
        hvacs_p = find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmd_p,
        )
        schedules_p = find_all("$.schedules[*]", rmd_p)
        annual_hours = get_schedule_year_length(context.BASELINE_0)

        return {
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids,
            "dict_of_zones_and_terminal_units_served_by_hvac_sys": dict_of_zones_and_terminal_units_served_by_hvac_sys,
            "schedules_p": schedules_p,
            "zones_p": zones_p,
            "hvacs_p": hvacs_p,
            "annual_hours": annual_hours,
        }

    def list_filter(self, context_item, data):
        hvac_sys_b = context_item.BASELINE_0
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return hvac_sys_b["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule46w18.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                manual_check_required_msg="The minimum volume flowrate is greater than the maximum of the minimum "
                "ventilation flowrate and 50% of the maximum supply flow rate.  This is "
                "correct IF the minimum volume flowrate is equal to any airflow required to "
                "comply with codes or accredidation standards, the system passes, "
                "otherwise it fails.  We are not able to determine the airflow required to "
                "comply with codes or accreditation standards at this time.",
                pass_msg="The minimum volume flowrate is equal to the maximum of the minimum ventilation flowrate and "
                "50% of the maximum supply flow rate.  If any airflow required to comply with codes or "
                "accredidation standards is MORE than this value, the minimum volume airflow should be set "
                "to this value.  We are not able to determine the airflow required to comply with codes or "
                "accreditation standards at this time, please double check that there are no additional "
                "codes or accreditation standards in regards to airflow. ",
                precision={
                    "minimum_airflow_b": {
                        "precision": 1,
                        "unit": "cfm",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            fan_system_b = hvac_b["fan_system"]
            min_volume_flowrate_b = getattr_(
                fan_system_b, "FanSystem", "minimum_airflow"
            )
            min_ventilation_flowrate_b = getattr_(
                fan_system_b, "FanSystem", "minimum_outdoor_airflow"
            )
            max_supply_flowrate_b = sum(
                [
                    supply_fan.get("design_airflow", ZERO.FLOW)
                    for supply_fan in find_all("$.supply_fans[*]", fan_system_b)
                ]
            )
            annual_hours = data["annual_hours"]
            zones_and_terminals_dict = data[
                "dict_of_zones_and_terminal_units_served_by_hvac_sys"
            ][hvac_b["id"]]
            zone_p = next(
                zone
                for zone in data["zones_p"]
                if zone["id"] == zones_and_terminals_dict["zone_list"][0]
            )
            min_volume_list_p = [0.0] * annual_hours
            for terminal_p in zone_p.get("terminals", []):

                if terminal_p.get("type") == TERMINAL_TYPE.BASEBOARD:
                    continue

                hvac_p = next(
                    hvac
                    for hvac in data["hvacs_p"]
                    if hvac["id"]
                    == getattr_(
                        terminal_p,
                        "Terminal",
                        "served_by_heating_ventilating_air_conditioning_system",
                    )
                )
                fan_system_p = hvac_p.get("fan_system", {})
                operation_schedule_hourly_values_p = next(
                    schedule_p
                    for schedule_p in data["schedules_p"]
                    if schedule_p["id"] == fan_system_p.get("operating_schedule")
                ).get("hourly_values", [1.0] * annual_hours)
                min_volume_p = getattr_(terminal_p, "Terminal", "minimum_airflow")

                for hour in range(len(operation_schedule_hourly_values_p)):
                    min_volume_list_p[hour] += (
                        min_volume_p * operation_schedule_hourly_values_p[hour]
                    )

            effective_min_volume_p = max(min_volume_list_p)
            reference_min_b = max(
                min_ventilation_flowrate_b,
                VENT_THRESHOLD_FACTOR * max_supply_flowrate_b,
            )

            return {
                "min_airflow_b": CalcQ("air_flow_rate", min_volume_flowrate_b),
                "min_ventilation_airflow_b": CalcQ(
                    "air_flow_rate", min_ventilation_flowrate_b
                ),
                "max_supply_airflow_b": CalcQ("air_flow_rate", max_supply_flowrate_b),
                "reference_min_b": CalcQ("air_flow_rate", reference_min_b),
                "effective_min_volume_p": CalcQ(
                    "air_flow_rate", effective_min_volume_p
                ),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            reference_min_b = calc_vals["reference_min_b"]
            effective_min_volume_p = calc_vals["effective_min_volume_p"]

            return effective_min_volume_p > reference_min_b

        def rule_check(self, context, calc_vals=None, data=None):
            min_airflow_b = calc_vals["min_airflow_b"]
            min_ventilation_airflow_b = calc_vals["min_ventilation_airflow_b"]
            reference_min_b = calc_vals["reference_min_b"]
            effective_min_volume_p = calc_vals["effective_min_volume_p"]

            return (
                self.precision_comparison["minimum_airflow_b"](
                    min_airflow_b, reference_min_b
                )
                and (
                    self.precision_comparison["minimum_airflow_b"](
                        effective_min_volume_p, reference_min_b
                    )
                    or effective_min_volume_p < reference_min_b
                )
                and not (
                    min_airflow_b
                    < max(
                        min_ventilation_airflow_b,
                        VENT_THRESHOLD_FACTOR * calc_vals["max_supply_airflow_b"],
                        effective_min_volume_p,
                    )
                )
            )
