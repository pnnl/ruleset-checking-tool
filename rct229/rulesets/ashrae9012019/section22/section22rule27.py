from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
]


class PRM9012019Rule86p62(RuleDefinitionListIndexedBase):
    """Rule 27 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule86p62, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule86p62.ChillerRule(),
            index_rmd=BASELINE_0,
            id="22-27",
            description="Each baseline chiller shall be modeled with separate condenser water pump interlocked to operate with the associated chiller.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="chillers[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule86p62.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["is_condenser_water_pump_interlocked"],
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.BASELINE_0
            is_condenser_water_pump_interlocked = chiller_b[
                "is_condenser_water_pump_interlocked"
            ]
            return {
                "is_condenser_water_pump_interlocked": is_condenser_water_pump_interlocked
            }

        def rule_check(self, context, calc_vals=None, data=None):
            is_condenser_water_pump_interlocked = calc_vals[
                "is_condenser_water_pump_interlocked"
            ]
            return is_condenser_water_pump_interlocked
