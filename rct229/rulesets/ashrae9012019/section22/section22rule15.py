from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_heat_rejection_loops_connected_to_baseline_systems import (
    get_heat_rejection_loops_connected_to_baseline_systems,
)
from rct229.schema.config import ureg
from rct229.utils.pint_utils import CalcQ
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)

TEMP_LOW_LIMIT_55F = 55 * ureg("degF")
TEMP_HIGH_LIMIT_90F = 90 * ureg("degF")
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

class Section22Rule15(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule15, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule15.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-15",
            description="The baseline heat rejection device shall have the approach calculated according to the equation 25.72 - (0.24*WB), valid for evaporation design wet-bulb temperatures from 55°F to 90°F.",
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

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_ids_b = (
            get_heat_rejection_loops_connected_to_baseline_systems(rmd_b)
        )

        return {"heat_rejection_loop_ids_b": heat_rejection_loop_ids_b}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule15.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["approach", "loop", "design_wetbulb_temperature"],
                },
                precision={
                    "approach_b": {
                        "precision": 0.1,
                        "unit": "K",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_loop_ids_b = data["heat_rejection_loop_ids_b"]
            heat_rejection_loop_b = heat_rejection_b["loop"]
            design_wetbulb_temp_b = heat_rejection_b["design_wetbulb_temperature"]

            return (
                heat_rejection_loop_b in heat_rejection_loop_ids_b
                and TEMP_LOW_LIMIT_55F <= design_wetbulb_temp_b <= TEMP_HIGH_LIMIT_90F
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            approach_b = heat_rejection_b["approach"]
            target_approach_b = 25.72 * ureg("degF") - (
                0.24 * heat_rejection_b["design_wetbulb_temperature"].to(ureg.F)
            )

            return {
                "approach_b": CalcQ("temperature_difference", approach_b),
                "target_approach_b": CalcQ("temperature_difference", target_approach_b),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            approach_b = calc_vals["approach_b"]
            target_approach_b = calc_vals["target_approach_b"]

            return self.precision_comparison["approach_b"](
                target_approach_b.to(ureg.kelvin), approach_b
            )
