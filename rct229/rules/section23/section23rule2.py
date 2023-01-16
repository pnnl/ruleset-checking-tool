from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.schema.config import ureg
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
]

FanSystemTemperatureControl = schema_enums["FanSystemTemperatureControlOptions"]
REQUIRED_RESET_DIFF_TEMP = 5.0 * ureg("degR")


class Section23Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section23Rule2.HeatingVentilatingAirConditioningSystemRule(),
            index_rmr="baseline",
            id="23-2",
            description="For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.12 Supply Air Temperature Reset (Systems 5 through 8 and 11)",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$..heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
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

    class HeatingVentilatingAirConditioningSystemRule(RuleDefinitionBase):
        def __init__(self):
            super(Section23Rule2.HeatingVentilatingAirConditioningSystemRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": ["temperature_control", "reset_differential_temperature"],
                },
            )

        def get_calc_vals(self, context, data=None):
            fan_system_b = context.baseline["fan_system"]
            temperature_control_b = fan_system_b["temperature_control"]
            reset_differential_temperature_b = fan_system_b[
                "reset_differential_temperature"
            ]
            return {
                "temperature_control_b": temperature_control_b,
                "reset_differential_temperature_b": CalcQ(
                    "temperature", reset_differential_temperature_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_control_b = calc_vals["temperature_control_b"]
            reset_differential_temperature_b = calc_vals[
                "reset_differential_temperature_b"
            ]
            return (
                temperature_control_b == FanSystemTemperatureControl.ZONE_RESET
                and std_equal(
                    reset_differential_temperature_b, REQUIRED_RESET_DIFF_TEMP
                )
            )
