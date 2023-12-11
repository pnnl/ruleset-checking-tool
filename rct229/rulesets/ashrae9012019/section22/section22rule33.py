from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
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


class Section22Rule33(RuleDefinitionBase):
    """Rule 33 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule33, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="22-33",
            description="Baseline chilled water system that does not use purchased chilled water must have no more than one CHW plant.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_list
                ]
            )
            and primary_secondary_loop_dict
        )

    def get_calc_vals(self, context, data=None):
        rmi_b = context.BASELINE_0
        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)
        num_primary_loops = len(primary_secondary_loop_dict)
        num_secondary_loops = sum(
            [
                len(primary_secondary_loop_dict[primary_loop])
                for primary_loop in primary_secondary_loop_dict
            ]
        )

        return {
            "num_primary_loops": num_primary_loops,
            "num_secondary_loops": num_secondary_loops,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        num_primary_loops = calc_vals["num_primary_loops"]
        num_secondary_loops = calc_vals["num_secondary_loops"]

        return num_primary_loops == 1 and num_secondary_loops == 1
