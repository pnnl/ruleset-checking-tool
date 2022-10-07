from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all

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


class Section22Rule23(RuleDefinitionListIndexedBase):
    """Rule 23 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule23, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule23.ChillerRule(),
            index_rmr="baseline",
            id="22-23",
            description="Each baseline chiller shall be modeled with separate chilled water pump interlocked to operate with the associated chiller.",
            rmr_context="ruleset_model_instances/0",
            list_path="chillers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11-1": ["hvac_sys_11_1"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        no_of_chillers_b = len(find_all("chillers[*]", rmi_b))

        primary_chw_loop_id_array = find_all("chillers[*].cooling_loop", rmi_b)
        primary_chw_loop_pump_num = 0
        for pump_b in find_all("pumps[*]", rmi_b):
            if pump_b["loop_or_piping"] in primary_chw_loop_id_array:
                primary_chw_loop_pump_num += 1
        return {
            "no_of_chillers_b": no_of_chillers_b,
            "primary_chw_loop_pump_num": primary_chw_loop_pump_num,
        }

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule23.ChillerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["is_chilled_water_pump_interlocked"],
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.baseline

            interlock_flag = False
            if chiller_b["is_chilled_water_pump_interlocked"]:
                interlock_flag = True
            return {"interlock_flag": interlock_flag}

        def rule_check(self, context, calc_vals=None, data=None):
            primary_chw_loop_pump_num = data["primary_chw_loop_pump_num"]
            interlock_flag = calc_vals["interlock_flag"]
            no_of_chillers_b = data["no_of_chillers_b"]
            return no_of_chillers_b == primary_chw_loop_pump_num and interlock_flag
