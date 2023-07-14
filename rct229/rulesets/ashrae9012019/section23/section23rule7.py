from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.utils.pint_utils import CalcQ

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_8,
]

TERMINAL_TEMPERATURE_CONTROL = schema_enums["TerminalTemperatureControlOptions"]


class Section23Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule7, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section23Rule7.HVACRule(),
            index_rmr="baseline",
            id="23-7",
            description="Systems 6&8: Supply air temperature setpoint shall be constant at the design condition.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        return {"applicable_hvac_sys_ids": applicable_hvac_sys_ids}

    def list_filter(self, context_item, data):
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return context_item.baseline["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section23Rule7.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "temperature_control",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline

            fan_system_b = hvac_b["fan_system"]
            temperature_control_b = fan_system_b["temperature_control"]

            return {
                "temperature_control_b": CalcQ("temperature", temperature_control_b),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_control_b = calc_vals["temperature_control_b"]

            return temperature_control_b == TERMINAL_TEMPERATURE_CONTROL.CONSTANT
