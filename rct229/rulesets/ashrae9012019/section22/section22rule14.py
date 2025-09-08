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
from rct229.schema.config import ureg
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

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
REQUIRED_TEMP_RANGE = 10 * ureg("degR")


class PRM9012019Rule95f90(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule95f90, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule95f90.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-14",
            description="The baseline heat rejection device shall have a design temperature rise of 10°F.",
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

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule95f90.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["range"],
                },
                precision={
                    "heat_rejection_range": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            heat_rejection_range = heat_rejection_b["range"]
            return {
                "heat_rejection_range": CalcQ(
                    "temperature_difference", heat_rejection_range
                ),
                "required_heat_rejection_range": CalcQ(
                    "temperature_difference", REQUIRED_TEMP_RANGE
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heat_rejection_range = calc_vals["heat_rejection_range"]
            required_heat_rejection_range = calc_vals["required_heat_rejection_range"]

            return self.precision_comparison["heat_rejection_range"](
                heat_rejection_range.to(ureg.kelvin),
                required_heat_rejection_range.to(ureg.kelvin),
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            heat_rejection_range = calc_vals["heat_rejection_range"]
            required_heat_rejection_range = calc_vals["required_heat_rejection_range"]

            return std_equal(
                heat_rejection_range.to(ureg.kelvin),
                required_heat_rejection_range.to(ureg.kelvin),
            )
