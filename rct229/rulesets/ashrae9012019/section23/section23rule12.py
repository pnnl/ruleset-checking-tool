from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
]


class PRM9012019Rule71k98(PartialRuleDefinition):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule71k98, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="23-12",
            description="System 11 in heating mode supply air temperature shall be modulated to maintain space temp and airflow shall be fixed at minimum airflow.",
            ruleset_section_title="HVAC - Airside",
            standard_section="G3.1.3.17 System 11 Supply Air Temperature and Fan Control",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0",
        )

    def applicability_check(self, context, calc_vals, data):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict_b = get_baseline_system_types(rmd_b)

        return any(
            [
                baseline_system_types_dict_b[system_type]
                and baseline_system_type_compare(
                    system_type, applicable_sys_type, False
                )
                for system_type in baseline_system_types_dict_b
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )
