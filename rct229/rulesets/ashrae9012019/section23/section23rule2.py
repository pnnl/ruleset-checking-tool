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
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
]

FanSystemTemperatureControl = SchemaEnums.schema_enums[
    "FanSystemTemperatureControlOptions"
]
REQUIRED_RESET_DIFF_TEMP = 5.0 * ureg("degR")


class PRM9012019Rule52x31(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule52x31, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule52x31.HVACRule(),
            index_rmd=BASELINE_0,
            id="23-2",
            description="For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.12 Supply Air Temperature Reset (Systems 5 through 8 and 11)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$..heating_ventilating_air_conditioning_systems[*]",
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
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
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

        return context_item.BASELINE_0["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule52x31.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "temperature_control",
                        "reset_differential_temperature",
                    ],
                },
                precision={
                    "reset_differential_temperature_b": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0

            fan_system_b = hvac_b["fan_system"]
            fan_system_id_b = fan_system_b["id"]
            temperature_control_b = fan_system_b["temperature_control"]
            reset_differential_temperature_b = fan_system_b[
                "reset_differential_temperature"
            ]

            return {
                "fan_system_id": fan_system_id_b,
                "temperature_control_b": temperature_control_b,
                "reset_differential_temperature_b": CalcQ(
                    "temperature_difference", reset_differential_temperature_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_control_b = calc_vals["temperature_control_b"]
            reset_differential_temperature_b = calc_vals[
                "reset_differential_temperature_b"
            ]

            return (
                temperature_control_b == FanSystemTemperatureControl.ZONE_RESET
                and self.precision_comparison["reset_differential_temperature_b"](
                    reset_differential_temperature_b,
                    REQUIRED_RESET_DIFF_TEMP,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
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
