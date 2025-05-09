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
from rct229.utils.assertions import getattr_
from rct229.utils.compare_standard_val import std_lt
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import find_exactly_one_terminal_unit

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_10,
]

REQ_DESIGN_SUPPLY_AIR_TEMP_SETPOINT = 105.0 * ureg("degF")


class PRM9012019Rule03j97(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule03j97, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule03j97.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-15",
            description="For baseline system types 9 & 10, the system design supply airflow rates shall be based on the temperature difference between a supply air temperature set point of 105°F and the design space-heating temperature set point, the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.8.2",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        zones_and_terminal_units_served_by_hvac_sys_dict = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )

        hvac_info_dict_b = {}
        for hvac_id_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmd_b,
        ):
            hvac_info_dict_b[hvac_id_b] = {
                "are_all_hvac_sys_fan_objs_autosized": are_all_hvac_sys_fan_objs_autosized(
                    rmd_b, hvac_id_b
                ),
                "all_design_setpoints_105": all(
                    [
                        std_equal(
                            REQ_DESIGN_SUPPLY_AIR_TEMP_SETPOINT.to(ureg.kelvin),
                            getattr_(
                                find_exactly_one_terminal_unit(rmd_b, terminal_id_b),
                                "Terminal",
                                "supply_design_heating_setpoint_temperature",
                            ).to(ureg.kelvin),
                        )
                        for terminal_id_b in zones_and_terminal_units_served_by_hvac_sys_dict[
                            hvac_id_b
                        ][
                            "terminal_unit_list"
                        ]
                    ]
                ),
                "proposed_supply_flow": sum(
                    [
                        terminal_p.get("primary_airflow", ZERO.FLOW)
                        for zone_id_b in zones_and_terminal_units_served_by_hvac_sys_dict[
                            hvac_id_b
                        ][
                            "zone_list"
                        ]
                        for terminal_p in find_all(
                            f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")].terminals[*]',
                            rmd_p,
                        )
                    ],
                    ZERO.FLOW,
                ),
            }

        return {
            "baseline_system_types_dict": baseline_system_types_dict,
            "hvac_info_dict_b": hvac_info_dict_b,
        }

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

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule03j97.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": ["minimum_outdoor_airflow"],
                },
                precision={
                    "supply_fan_airflow_b": {
                        "precision": 1,
                        "unit": "cfm",
                    },
                    "proposed_supply_flow": {
                        "precision": 1,
                        "unit": "cfm",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            baseline_system_types_dict = data["baseline_system_types_dict"]

            return any(
                hvac_id_b in baseline_system_types_dict[system_type]
                for system_type in APPLICABLE_SYS_TYPES
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            fan_system_b = hvac_b["fan_system"]

            fan_info_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_system_b
                )
            )

            supply_fan_qty_b = fan_info_b["supply_fans_qty"]
            supply_fan_airflow_b = fan_info_b["supply_fans_airflow"]

            minimum_outdoor_airflow_b = fan_system_b["minimum_outdoor_airflow"]

            return {
                "hvac_id_b": hvac_id_b,
                "supply_fan_qty_b": supply_fan_qty_b,
                "supply_fan_airflow_b": CalcQ("air_flow_rate", supply_fan_airflow_b),
                "minimum_outdoor_airflow_b": CalcQ(
                    "air_flow_rate", minimum_outdoor_airflow_b
                ),
                "all_design_setpoints_105": data["hvac_info_dict_b"][hvac_id_b][
                    "all_design_setpoints_105"
                ],
                "proposed_supply_flow": CalcQ(
                    "air_flow_rate",
                    data["hvac_info_dict_b"][hvac_id_b]["proposed_supply_flow"],
                ),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            supply_fan_qty_b = calc_vals["supply_fan_qty_b"]
            supply_fan_airflow_b = calc_vals["supply_fan_airflow_b"]
            all_design_setpoints_105 = calc_vals["all_design_setpoints_105"]
            proposed_supply_flow = calc_vals["proposed_supply_flow"]

            return (
                supply_fan_qty_b == 1
                and not all_design_setpoints_105
                and self.precision_comparison["proposed_supply_flow"](
                    proposed_supply_flow,
                    supply_fan_airflow_b,
                )
            ) or (supply_fan_qty_b != 1)

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_id_b = calc_vals["hvac_id_b"]
            supply_fan_qty_b = calc_vals["supply_fan_qty_b"]
            supply_fan_airflow_b = calc_vals["supply_fan_airflow_b"]
            all_design_setpoints_105 = calc_vals["all_design_setpoints_105"]
            proposed_supply_flow = calc_vals["proposed_supply_flow"]

            if (
                supply_fan_qty_b == 1
                and not all_design_setpoints_105
                and self.precision_comparison["proposed_supply_flow"](
                    proposed_supply_flow,
                    supply_fan_airflow_b,
                )
            ):
                # Case 3
                undetermined_msg = f"{hvac_id_b} was not modeled with a supply air temperature set point of 105°F. The baseline and proposed supply cfm was modeled identically at {proposed_supply_flow * ureg('cfm')} CFM. Manual review is required to determine if the airflow rate was modeled to comply with applicable codes or accreditation standards. If not, fail."
            else:
                # Case 4
                undetermined_msg = f"{hvac_id_b} doesn't have one supply fan associated with the HVAC system in the baseline and therefore this check could not be conducted for this HVAC sytem. Conduct manual check for compliance with G3.1.2.8.2."

            return undetermined_msg

        def rule_check(self, context, calc_vals=None, data=None):
            hvac_id_b = calc_vals["hvac_id_b"]
            supply_fan_qty_b = calc_vals["supply_fan_qty_b"]
            supply_fan_airflow_b = calc_vals["supply_fan_airflow_b"]
            minimum_outdoor_airflow_b = calc_vals["minimum_outdoor_airflow_b"]
            all_design_setpoints_105 = data["hvac_info_dict_b"][hvac_id_b][
                "all_design_setpoints_105"
            ]

            return supply_fan_qty_b == 1 and (
                (
                    all_design_setpoints_105
                    and supply_fan_airflow_b > minimum_outdoor_airflow_b
                )
                or (
                    not all_design_setpoints_105
                    and self.precision_comparison["supply_fan_airflow_b"](
                        minimum_outdoor_airflow_b, supply_fan_airflow_b
                    )
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            hvac_id_b = calc_vals["hvac_id_b"]
            supply_fan_qty_b = calc_vals["supply_fan_qty_b"]
            supply_fan_airflow_b = calc_vals["supply_fan_airflow_b"]
            minimum_outdoor_airflow_b = calc_vals["minimum_outdoor_airflow_b"]
            all_design_setpoints_105 = data["hvac_info_dict_b"][hvac_id_b][
                "all_design_setpoints_105"
            ]

            return supply_fan_qty_b == 1 and (
                (
                    all_design_setpoints_105
                    and std_lt(
                        val=supply_fan_airflow_b, std_val=minimum_outdoor_airflow_b
                    )
                )
                or (
                    not all_design_setpoints_105
                    and std_equal(minimum_outdoor_airflow_b, supply_fan_airflow_b)
                )
            )
