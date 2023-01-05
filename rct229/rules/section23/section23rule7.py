from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.pint_utils import CalcQ

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_8A,
    HVAC_SYS.SYS_8B,
]

TERMINAL_TEMPERATURE_CONTROL = schema_enums["TerminalTemperatureControlOptions"]


class Section23Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule7, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section23Rule7.FanSystemRule(),
            index_rmr="baseline",
            id="23-7",
            description="Systems 6&8: Supply air temperature setpoint shall be constant at the design condition.",
            rmr_context="ruleset_model_instances/0",
            list_path="$..fan_system",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_sys_types = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_sys_types
            ]
        )

    class FanSystemRule(RuleDefinitionBase):
        def __init__(self):
            super(Section23Rule7.FanSystemRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": [
                        "temperature_control",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fan_system_b = context.baseline
            temperature_control_b = fan_system_b["temperature_control"]

            return {
                "temperature_control_b": CalcQ("temperature", temperature_control_b),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_control_b = calc_vals["temperature_control_b"]

            return temperature_control_b == TERMINAL_TEMPERATURE_CONTROL.CONSTANT
