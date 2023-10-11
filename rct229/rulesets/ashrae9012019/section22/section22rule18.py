from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)

HEATREJECTIONFANSPEEDCONTROL = schema_enums["HeatRejectionFanSpeedControlOptions"]


class Section22Rule18(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule18, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule18.HeatRejectionRule(),
            index_rmr="baseline",
            id="22-18",
            description="The baseline heat rejection device shall be modeled with variable speed fan control.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.baseline

        return {
            "heat_rejection_loop_ids_b": get_heat_rejection_loops_connected_to_baseline_systems(
                rmd_b
            )
        }

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule18.HeatRejectionRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["fan_speed_control", "loop"],
                },
            )

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.baseline
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]
            heat_rejection_loop_b = heat_rejection_b["loop"]

            return heat_rejection_loop_b in heat_rejection_loop_ids_b

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.baseline
            fan_speed_control_b = heat_rejection_b["fan_speed_control"]

            return {
                "fan_speed_control_b": fan_speed_control_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            fan_speed_control_b = calc_vals["fan_speed_control_b"]

            return fan_speed_control_b == HEATREJECTIONFANSPEEDCONTROL.VARIABLE_SPEED
