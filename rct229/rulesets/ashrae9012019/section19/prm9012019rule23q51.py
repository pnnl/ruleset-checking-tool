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
from rct229.utils.jsonpath_utils import find_one

APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_1, HVAC_SYS.SYS_2, HVAC_SYS.SYS_9, HVAC_SYS.SYS_10]

AIR_ECONOMIZER = SchemaEnums.schema_enums["AirEconomizerOptions"]


class PRM9012019Rule23q51(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule23q51, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule23q51.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-9",
            description="Air economizers shall not be included in baseline HVAC Systems 1, 2, 9, and 10.",
            ruleset_section_title="HVAC - General",
            standard_section="G3.1.2.6",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return {
            "baseline_system_types_dict": {
                system_type: system_list
                for system_type, system_list in baseline_system_types_dict.items()
                if system_type in APPLICABLE_SYS_TYPES and system_list
            }
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule23q51.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": [
                        "fan_system",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            baseline_system_types_dict = data["baseline_system_types_dict"]

            return any(
                hvac_id_b in baseline_system_types_dict[system_type]
                for system_type in baseline_system_types_dict
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            fan_system_b = hvac_b["fan_system"]

            air_economizer_type_b = find_one("$.air_economizer.type", fan_system_b)

            return {
                "air_economizer_type_b": air_economizer_type_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            air_economizer_type_b = calc_vals["air_economizer_type_b"]

            return (
                air_economizer_type_b is None
                or air_economizer_type_b == AIR_ECONOMIZER.FIXED_FRACTION
            )
