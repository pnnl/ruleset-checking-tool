from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule99f07(RuleDefinitionBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule99f07, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="22-12",
            description="The heat rejection system shall be a single loop, modeled with a single cooling tower.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return heat_rejection_loop_ids_b

    def get_calc_vals(self, context, data=None):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        number_of_baseline_heat_rejections_b = len(
            [
                heat_rejection_b
                for heat_rejection_b in find_all("$.heat_rejections[*]", rmd_b)
                if getattr_(heat_rejection_b, "heat_rejections", "loop")
                in heat_rejection_loop_ids_b
            ]
        )

        return {
            "heat_rejection_loop_ids_b": heat_rejection_loop_ids_b,
            "number_of_baseline_heat_rejections_b": number_of_baseline_heat_rejections_b,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        heat_rejection_loop_ids_b = calc_vals["heat_rejection_loop_ids_b"]
        number_of_baseline_heat_rejections_b = calc_vals[
            "number_of_baseline_heat_rejections_b"
        ]

        return (
            number_of_baseline_heat_rejections_b == 1
            and len(heat_rejection_loop_ids_b) == 1
        )

    def get_fail_msg(self, context, calc_vals=None, data=None):
        heat_rejection_loop_ids_b = calc_vals["heat_rejection_loop_ids_b"]
        number_of_baseline_heat_rejections_b = calc_vals[
            "number_of_baseline_heat_rejections_b"
        ]
        len_heat_rejection_loop_ids_b = len(heat_rejection_loop_ids_b)

        if (
            number_of_baseline_heat_rejections_b == 1
            and len_heat_rejection_loop_ids_b > 1
        ):
            FAIL_MSG = "There is more than one condenser loop for this project. There should only be one condenser loop attached to all chillers in the baseline chiller plant."
        elif (
            number_of_baseline_heat_rejections_b > 1
            and len_heat_rejection_loop_ids_b == 1
        ):
            FAIL_MSG = "There is more than one cooling tower for the baseline chiller plant. There should only be one cooling tower attached to the condenser loop."
        else:
            FAIL_MSG = (
                "There is more than one cooling tower on this loop and there is more than one condenser loop for the chiller plant. "
                "For the baseline chiller plant, there should be only one condenser loop with only one cooling tower."
            )

        return FAIL_MSG
