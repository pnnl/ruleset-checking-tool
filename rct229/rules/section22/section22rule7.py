from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
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


class Section22Rule7(RuleDefinitionBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule7, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            id="22-7",
            description="Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.",
            rmr_context="ruleset_model_instances/0",
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

    def get_calc_vals(self, context, data=None):
        rmi_b = context.baseline
        primary_secondary_loop_dictionary = get_primary_secondary_loops_dict(rmi_b)

        return {"primary_secondary_loop_dictionary": primary_secondary_loop_dictionary}

    def rule_check(self, context, calc_vals=None, data=None):
        primary_secondary_loop_dictionary = calc_vals[
            "primary_secondary_loop_dictionary"
        ]

        return len(primary_secondary_loop_dictionary) != 0
