import math

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_

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
REQUIRED_BUILDING_PEAK_LOAD_300 = 300 * ureg("ton")
REQUIRED_BUILDING_PEAK_LOAD_600 = 600 * ureg("ton")
CHILLER_SIZE_800 = 800 * ureg("ton")


class PRM9012019Rule30m88(RuleDefinitionBase):
    """Rule 31 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule30m88, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="22-31",
            description="The baseline chiller plant shall be modeled with the chiller quantity specified in Table G3.1.3.7, as a function of building peak cooling load.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.1 Type and Number of Chillers (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            required_fields={
                "$": ["model_output"],
            },
            precision={
                "building_peak_load_b": {
                    "precision": 1,
                    "unit": "ton",
                },
            },
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
        chiller_number = len(rmd_b["chillers"])

        output_b = rmd_b["model_output"]
        building_peak_load_b = getattr_(
            output_b,
            "building_peak_cooling_load",
            "building_peak_cooling_load",
        )

        if (
            building_peak_load_b < REQUIRED_BUILDING_PEAK_LOAD_300
            or self.precision_comparison["building_peak_load_b"](
                building_peak_load_b,
                REQUIRED_BUILDING_PEAK_LOAD_300,
            )
        ):
            target_chiller_number = 1
        elif building_peak_load_b < REQUIRED_BUILDING_PEAK_LOAD_600:
            target_chiller_number = 2
        else:
            target_chiller_number = max(
                2, math.ceil(building_peak_load_b / CHILLER_SIZE_800)
            )

        return {
            "chiller_number": chiller_number,
            "target_chiller_number": target_chiller_number,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        chiller_number = calc_vals["chiller_number"]
        target_chiller_number = calc_vals["target_chiller_number"]

        return chiller_number == target_chiller_number
