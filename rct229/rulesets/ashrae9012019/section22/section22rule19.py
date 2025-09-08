from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

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
TEMPERATURE_RESET = SchemaEnums.schema_enums["TemperatureResetOptions"]


class PRM9012019Rule68h16(RuleDefinitionListIndexedBase):
    """Rule 19 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule68h16, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule68h16.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-19",
            description="The baseline heat rejection device shall be controlled to maintain a constant leaving water temperature.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="heat_rejections[*]",
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

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_dict = {
            heat_rejection_loop_id: find_exactly_one_with_field_value(
                "$.fluid_loops[*]", "id", heat_rejection_loop_id, rmd_b
            )
            for heat_rejection_loop_id in find_all("$.heat_rejections[*].loop", rmd_b)
        }
        return {"heat_rejection_loop_dict": heat_rejection_loop_dict}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule68h16.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            loop_b = heat_rejection_b["loop"]
            temperature_reset_type = getattr_(
                data["heat_rejection_loop_dict"][loop_b],
                "temperature_reset_type",
                "cooling_or_condensing_design_and_control",
                "temperature_reset_type",
            )
            return {"temperature_reset_type": temperature_reset_type}

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_reset_type = calc_vals["temperature_reset_type"]
            return temperature_reset_type == TEMPERATURE_RESET.NO_RESET
