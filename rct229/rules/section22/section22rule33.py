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
    HVAC_SYS.SYS_11B,
    HVAC_SYS.SYS_12B,
    HVAC_SYS.SYS_13B,
]


class Section22Rule33(RuleDefinitionListIndexedBase):
    """Rule 33 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule33, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule33.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-33",
            description="Baseline chilled water system that does not use purchased chilled water must only have no more than one CHW plant.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
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
        # primary_secondary_loop_dictionary = get_primary_secondary_loops(rmi_b) # TODO this should be updated!!
        len_primary_secondary_loop_dictionary = 1
        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_lists
                ]
            )
            and True
            if len(len_primary_secondary_loop_dictionary) != 0
            else False
        )

    def get_calc_vals(self, context, data=None):
        rmi_b = context.baseline
        # primary_secondary_loop_dictionary = get_primary_secondary_loops(rmi_b) # TODO this should be updated!!
        primary_secondary_loop_dictionary = {"Primary1": ["secondary1", "secondary2"]}
        num_primary_loops = len(primary_secondary_loop_dictionary)
        num_secondary_loops = sum(
            [
                primary_secondary_loop_dictionary[primary_loop]
                for primary_loop in primary_secondary_loop_dictionary.keys()
            ]
        )
        return {
            "num_primary_loops ": num_primary_loops,
            "num_secondary_loops": num_secondary_loops,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        num_primary_loops = calc_vals["num_primary_loops"]
        num_secondary_loops = calc_vals["num_secondary_loops"]
        return num_primary_loops == 1 and num_secondary_loops == 1
