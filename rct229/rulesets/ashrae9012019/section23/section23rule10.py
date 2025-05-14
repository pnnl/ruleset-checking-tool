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
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
]

FAN_SYSTEM_SUPPLY_FAN_VOLUME_RESET = SchemaEnums.schema_enums[
    "FanSystemSupplyFanVolumeResetOptions"
]

FAN_SYSTEM_SUPPLY_FAN_VOLUME_RESET_FRACTION = 0.5


class PRM9012019Rule18u93(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule18u93, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule18u93.HVACRule(),
            index_rmd=BASELINE_0,
            id="23-10",
            description="System 11 Fan volume shall be reset from 100% airflow at 100% cooling load to minimum "
            "airflow at 50% cooling load. ",
            ruleset_section_title="HVAC - Airside",
            standard_section="G3.1.3.17 System 11 Supply Air Temperature and Fan Control",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # if baseline does not have system 3-8 or 11, 12, 13, then this rule is not applicable
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

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule18u93.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                precision={
                    "fan_volume_reset_fraction_b": {
                        "precision": 0.1,
                    },
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]
            return hvac_b["id"] in applicable_hvac_sys_ids

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            fan_system_b = hvac_b["fan_system"]

            return {
                "fan_volume_reset_fraction": fan_system_b.get(
                    "fan_volume_reset_fraction"
                ),
                "fan_volume_reset_type": fan_system_b.get("fan_volume_reset_type"),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            fan_volume_reset_fraction_b = calc_vals["fan_volume_reset_fraction"]
            fan_volume_reset_type_b = calc_vals["fan_volume_reset_type"]

            return (
                fan_volume_reset_type_b
                == FAN_SYSTEM_SUPPLY_FAN_VOLUME_RESET.DESIGN_LOAD_RESET
                and self.precision_comparison["fan_volume_reset_fraction_b"](
                    fan_volume_reset_fraction_b,
                    FAN_SYSTEM_SUPPLY_FAN_VOLUME_RESET_FRACTION,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            fan_volume_reset_fraction_b = calc_vals["fan_volume_reset_fraction"]
            fan_volume_reset_type_b = calc_vals["fan_volume_reset_type"]

            return (
                fan_volume_reset_type_b
                == FAN_SYSTEM_SUPPLY_FAN_VOLUME_RESET.DESIGN_LOAD_RESET
                and std_equal(
                    fan_volume_reset_fraction_b,
                    FAN_SYSTEM_SUPPLY_FAN_VOLUME_RESET_FRACTION,
                )
            )
