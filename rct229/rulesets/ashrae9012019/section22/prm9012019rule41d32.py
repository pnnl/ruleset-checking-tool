from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_fluid_loop

FLUID_LOOP_FLOW_CONTROL = SchemaEnums.schema_enums["FluidLoopFlowControlOptions"]


class PRM9012019Rule41d32(RuleDefinitionListIndexedBase):
    """Rule 28 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule41d32, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule41d32.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-28",
            description="The baseline building design condenser water pump shall be modeled as constant volume.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        return bool(find_all("$.heat_rejections[*]", rmd_b))

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        fluid_loop_b = {
            heat_rej_b["id"]: find_exactly_one_fluid_loop(
                rmd_b, getattr_(heat_rej_b, "heat_rejections", "loop")
            )
            for heat_rej_b in find_all("$.heat_rejections[*]", rmd_b)
        }

        return {
            "heat_rejection_loop_ids_b": heat_rejection_loop_ids_b,
            "fluid_loop_b": fluid_loop_b,
        }

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule41d32.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                )
            )

        def is_applicable(self, context, data=None):
            heat_rej_b = context.BASELINE_0
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]
            heat_rejection_loop_b = heat_rej_b["loop"]

            return heat_rejection_loop_b in heat_rejection_loop_ids_b

        def get_calc_vals(self, context, data=None):
            heat_rej_b = context.BASELINE_0
            heat_rej_id_b = heat_rej_b["id"]
            heat_rej_fluid_loop_b = data["fluid_loop_b"][heat_rej_id_b]

            heat_rejection_flow_ctrl_b = getattr_(
                heat_rej_fluid_loop_b,
                "heat_rejections",
                "cooling_or_condensing_design_and_control",
                "flow_control",
            )

            return {
                "heat_rejection_flow_ctrl_b": heat_rejection_flow_ctrl_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heat_rejection_flow_ctrl_b = calc_vals["heat_rejection_flow_ctrl_b"]

            return heat_rejection_flow_ctrl_b == FLUID_LOOP_FLOW_CONTROL.FIXED_FLOW
