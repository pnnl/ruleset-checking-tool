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
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_10,
]

REQ_DESIGN_SUPPLY_AIR_TEMP_SETPOINT = 105.0 * ureg("degF")


class Section19Rule17(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule17, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section19Rule17.HVACRule(),
            index_rmr="baseline",
            id="19-17",
            description="For baseline system types 9 & 10, the system design supply airflow rates shall be based on the temperature difference between a supply air temperature set point of 105°F and the design space-heating temperature set point, the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.8.2",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        rmi_p = context.proposed
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        hvac_info_dict_b = {}
        for hvac_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmi_b,
        ):
            hvac_info_dict_b[hvac_b["id"]] = {}

            zones_and_terminal_units_served_by_hvac_sys_dict = (
                get_dict_of_zones_and_terminal_units_served_by_hvac_sys(hvac_b)
            )

            all_design_setpoints_105 = True
            proposed_supply_cfm = ZERO.FLOW
            for terminal_b in zones_and_terminal_units_served_by_hvac_sys_dict[
                "terminal_unit_list"
            ]:
                for terminal in find_all(
                    f'$.buildings[*].building_segments[*].zones[*].terminals[?(@.id == "{terminal_b}")]',
                    rmi_b,
                ):
                    if (
                        getattr_(
                            terminal,
                            "Terminal",
                            "supply_design_heating_setpoint_temperature",
                        )
                        != REQ_DESIGN_SUPPLY_AIR_TEMP_SETPOINT
                    ):
                        all_design_setpoints_105 = False

            for zone_b in zones_and_terminal_units_served_by_hvac_sys_dict["zone_lsit"]:
                for terminal_p in find_one(
                    f"$.buildings[*].building_segments[*].zones[?(@.id == {zone_b})].terminals[*]",
                    rmi_p,
                ):
                    proposed_supply_cfm += getattr_(
                        terminal_p, "Terminal", "primary_airflow"
                    )

        return {
            "baseline_system_types_dict": baseline_system_types_dict,
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
            super(Section19Rule17.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            baseline_system_types_dict = data["baseline_system_types_dict"]

            return any(
                hvac_id_b in baseline_system_types_dict[system_type]
                for system_type in baseline_system_types_dict.keys()
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]

            return {}

        def rule_check(self, context, calc_vals=None, data=None):
            return ()
