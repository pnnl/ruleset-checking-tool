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
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import CalcQ

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_4,
]


class PRM9012019Rule40y63(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule40y63, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule40y63.HVACRule(),
            index_rmd=BASELINE_0,
            id="23-17",
            description="System 2 and 4 - Electric air-source heat pumps shall shall be modeled to continue to operate while auxiliary heat is energized.",
            ruleset_section_title="HVAC - Airside",
            standard_section="G3.1.3.1 Heat Pumps (Systems 2 and 4)",
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
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        return {
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids,
            "baseline_system_types_dict": baseline_system_types_dict,
        }

    def list_filter(self, context_item, data):
        hvac_sys_b = context_item.BASELINE_0
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return hvac_sys_b["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule40y63.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["heating_system"],
                },
                precision={
                    "heatpump_low_shutoff_b": {
                        "precision": 0.1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            baseline_system_types_dict = data["baseline_system_types_dict"]

            heating_system_b = hvac_b["heating_system"]
            heatpump_low_shutoff_b = getattr_(
                heating_system_b, "HeatingSystem", "heatpump_low_shutoff_temperature"
            )
            return {
                "heatpump_low_shutoff_temperature": CalcQ(
                    "temperature", heatpump_low_shutoff_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heatpump_low_shutoff_b = calc_vals["heatpump_low_shutoff_temperature"]
            # The heat pump low shutoff temperature equal to the flag of -999, which indicates that there is no low-temperature shutoff for the heatpump
            # The minimum temperature is not finalized and is up for discussion.  Must coordinate with the note provided in the schema element: HeatingSystem.heatpump_low_shutoff_temperature
            return heatpump_low_shutoff_b <= -999 * ureg("F")
