from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types

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


class Section22Rule27(RuleDefinitionListIndexedBase):
    """Rule 27 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule27, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule27.ChillerRule(),
            index_rmr="baseline",
            id="22-27",
            description="Each baseline chiller shall be modeled with separate condenser-water pump interlocked to operate with the associated chiller.",
            rmr_context="ruleset_model_instances/0",
            list_path="chillers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_type_lists = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_lists
            ]
        )

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule27.ChillerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["is_condenser_water_pump_interlocked"],
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.baseline
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
