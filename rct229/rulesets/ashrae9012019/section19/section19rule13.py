from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
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
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

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
            standard_section="G3.1.2.8.1 and Exception 1",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys = 1

        design_thermostat_cooling_setpoint = min(
            find_all(
                "$.buildings[*].building_segments[*].zones[*].design_thermostat_cooling_setpoint",
                rmi_b,
            )
        )
        design_thermostat_heating_setpoint = max(
            find_all(
                "$.buildings[*].building_segments[*].zones[*].design_thermostat_heating_setpoint",
                rmi_b,
            )
        )

        return {
            "dict_of_zones_and_terminal_units_served_by_hvac_sys_b": get_dict_of_zones_and_terminal_units_served_by_hvac_sys(
                rmi_b
            ),
            "design_thermostat_cooling_setpoint": design_thermostat_cooling_setpoint,
            "design_thermostat_heating_setpoint": design_thermostat_heating_setpoint,
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
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            dict_of_zones_and_terminal_units_served_by_hvac_sys_b = data[
                "dict_of_zones_and_terminal_units_served_by_hvac_sys_b"
            ]

            hvac_id_b = hvac_b["id"]

            zones_list_hvac_sys_b = (
                dict_of_zones_and_terminal_units_served_by_hvac_sys_b[hvac_id_b][
                    "zone_list"
                ]
            )
            terminal_list_hvac_sys_b = (
                dict_of_zones_and_terminal_units_served_by_hvac_sys_b[hvac_id_b][
                    "terminal_list"
                ]
            )

            return True

        def rule_check(self, context, calc_vals=None, data=None):
            return True
