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
from rct229.utils.jsonpath_utils import find_all, find_one

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_12B,
]
NOT_APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_1A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_11_1C,
]
TEMP_RESET_TYPE = SchemaEnums.schema_enums["TemperatureResetOptions"]


class PRM9012019Rule58a51(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule58a51, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule58a51.ChillerFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-3",
            description="Baseline chilled water loops that do not use purchased cooling and do not serve any computer rooms (i.e., do not serve baseline system type 11) shall have the chilled water supply temperature reset based on outdoor dry-bulb temperature.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
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
        ) and any(
            [
                available_type not in NOT_APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        chiller_loop_ids_list = find_all("$.chillers[*].cooling_loop", rmd_b)
        return {"chiller_loop_ids": chiller_loop_ids_list}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        loop_chiller_ids_list = data["chiller_loop_ids"]
        return fluid_loop_b["id"] in loop_chiller_ids_list

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule58a51.ChillerFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            temperature_reset_type = find_one(
                "$.cooling_or_condensing_design_and_control.temperature_reset_type",
                fluid_loop_b,
            )
            return {"temperature_reset_type": temperature_reset_type}

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_reset_type = calc_vals["temperature_reset_type"]
            return temperature_reset_type == TEMP_RESET_TYPE.OUTSIDE_AIR_RESET
