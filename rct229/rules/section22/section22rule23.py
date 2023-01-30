from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.jsonpath_utils import find_all

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


class Section22Rule23(RuleDefinitionBase):
    """Rule 23 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule23, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            id="22-23",
            description="Each baseline chiller shall be modeled with separate chilled water pump interlocked to operate with the associated chiller.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def get_calc_vals(self, context, data=None):
        rmi_b = context.baseline
        num_of_chillers_b = len(find_all("$.chillers[*]", rmi_b))
        primary_chw_loop_id_array = find_all("$.chillers[*].cooling_loop", rmi_b)
        interlock_flag = all(
            find_all("$.chillers[*].is_chilled_water_pump_interlocked", rmi_b)
        )

        primary_chw_loop_pump_num = len(
            [
                pump_b
                for pump_b in find_all("$.pumps[*]", rmi_b)
                if pump_b["loop_or_piping"] in primary_chw_loop_id_array
            ]
        )

        return {
            "num_of_chillers_b": num_of_chillers_b,
            "primary_chw_loop_pump_num": primary_chw_loop_pump_num,
            "interlock_flag": interlock_flag,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        num_of_chillers_b = calc_vals["num_of_chillers_b"]
        primary_chw_loop_pump_num = calc_vals["primary_chw_loop_pump_num"]
        interlock_flag = calc_vals["interlock_flag"]

        return num_of_chillers_b == primary_chw_loop_pump_num and interlock_flag
