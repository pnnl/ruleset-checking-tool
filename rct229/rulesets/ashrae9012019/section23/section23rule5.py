from pydash import flatten
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.utils.assertions import getattr_

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_8,
]


class PRM9012019Rule69z86(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule69z86, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule69z86.TerminalRule(),
            index_rmd=BASELINE_0,
            id="23-5",
            description="For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall run as the first stage of heating before the reheat coil is energized.",
            ruleset_section_title="HVAC - Airside",
            standard_section="G3.1.3.14 Fan Power and Control (Systems 6 and 8)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].zones[*].terminals[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        hvac_sys_6_or_8_list = flatten(
            [
                baseline_system_types_dict[system_type]
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
                if baseline_system_types_dict[system_type]
                and baseline_system_type_compare(
                    system_type, applicable_sys_type, False
                )
            ]
        )

        return {
            "hvac_sys_6_or_8_list": hvac_sys_6_or_8_list,
        }

    class TerminalRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule69z86.TerminalRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def is_applicable(self, context, data=None):
            terminal_b = context.BASELINE_0
            hvac_sys_6_or_8_list = data["hvac_sys_6_or_8_list"]
            served_by_hvac_b = getattr_(
                terminal_b,
                "terminals",
                "served_by_heating_ventilating_air_conditioning_system",
            )

            return served_by_hvac_b in hvac_sys_6_or_8_list

        def get_calc_vals(self, context, data=None):
            terminal_b = context.BASELINE_0
            is_fan_first_stage_heat_b = getattr_(
                terminal_b, "terminals", "is_fan_first_stage_heat"
            )

            return {"is_fan_first_stage_heat_b": is_fan_first_stage_heat_b}

        def rule_check(self, context, calc_vals=None, data={}):
            is_fan_first_stage_heat_b = calc_vals["is_fan_first_stage_heat_b"]

            return is_fan_first_stage_heat_b
