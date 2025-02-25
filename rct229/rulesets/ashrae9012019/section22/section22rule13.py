from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_

HEATREJECTIONFAN = SchemaEnums.schema_enums["HeatRejectionFanOptions"]
HEATREJECTION = SchemaEnums.schema_enums["HeatRejectionOptions"]
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


class Section22Rule13(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule13, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule13.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-13",
            description="The baseline heat rejection device shall be an axial-fan open circuit cooling tower.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def create_data(self, context, data=None):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return {"heat_rejection_loop_ids_b": heat_rejection_loop_ids_b}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule13.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_type", "type"],
                },
            )

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_loop_b = getattr_(
                heat_rejection_b, "heat_rejections", "loop"
            )
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]

            return heat_rejection_loop_b in heat_rejection_loop_ids_b

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            fan_type_b = heat_rejection_b["fan_type"]
            heat_rejection_type_b = heat_rejection_b["type"]

            return {
                "fan_type_b": fan_type_b,
                "heat_rejection_type_b": heat_rejection_type_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            fan_type_b = calc_vals["fan_type_b"]
            heat_rejection_type_b = calc_vals["heat_rejection_type_b"]

            return (
                fan_type_b == HEATREJECTIONFAN.AXIAL
                and heat_rejection_type_b == HEATREJECTION.OPEN_CIRCUIT_COOLING_TOWER
            )
