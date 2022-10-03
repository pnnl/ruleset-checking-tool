from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-11.1",
    "SYS-11.2",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-11B",
    "SYS-12B",
    "SYS-13B",
]


class Section22Rule27(RuleDefinitionListIndexedBase):
    """Rule 27 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule27, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule27.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-27",
            description="Each baseline chiller shall be modeled with separate condenser-water pump interlocked to operate with the associated chiller.",
            rmr_context="ruleset_model_instances/0",
            list_path="chillers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11.1": ["hvac_sys_11_1"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule27.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["is_condenser_water_pump_interlocked"],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            is_condenser_water_pump_interlocked = fluid_loop_b[
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
