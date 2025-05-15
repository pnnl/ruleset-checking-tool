from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12A,
    HVAC_SYS.SYS_1B,
    HVAC_SYS.SYS_3B,
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_9B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
    HVAC_SYS.SYS_1C,
    HVAC_SYS.SYS_3C,
    HVAC_SYS.SYS_7C,
    HVAC_SYS.SYS_8C,
    HVAC_SYS.SYS_11_1C,
]
HEATING = SchemaEnums.schema_enums["FluidLoopOptions"].HEATING


class PRM9012019Rule31d63(RuleDefinitionBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule31d63, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="21-16",
            description="Baseline shall have only one heating hot water plant.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
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

    def get_calc_vals(self, context, data=None):
        rmd_b = context.BASELINE_0
        hhw_loop_count = len(
            find_all('$..fluid_loops[*][?(@.type = "HEATING")]', rmd_b)
        )
        return {"hhw_loop_count": hhw_loop_count}

    def rule_check(self, context, calc_vals=None, data=None):
        hhw_loop_count = calc_vals["hhw_loop_count"]
        return hhw_loop_count == 1
