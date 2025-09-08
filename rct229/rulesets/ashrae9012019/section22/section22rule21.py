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
from rct229.schema.schema_enums import SchemaEnums
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
CHILLER_COMPRESSOR = SchemaEnums.schema_enums["ChillerCompressorOptions"]
REQUIRED_BUILDING_PEAK_LOAD_600 = 600 * ureg("ton")


class PRM9012019Rule96z66(RuleDefinitionListIndexedBase):
    """Rule 21 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule96z66, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule96z66.ChillerRule(),
            index_rmd=BASELINE_0,
            id="22-21",
            description="The baseline chiller plant shall be modeled with chiller(s) having the type as indicated in Table G3.1.3.7 as a function of building peak cooling load.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.1 Type and Number of Chillers (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.chillers[*]",
            required_fields={
                "$": ["model_output"],
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

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        output_b = rmd_b["model_output"]
        building_cooling_peak_load = getattr_(
            output_b,
            "building_peak_cooling_load",
            "building_peak_cooling_load",
        )

        return {"building_cooling_peak_load": building_cooling_peak_load}

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule96z66.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["compressor_type"],
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.BASELINE_0
            compressor_type = chiller_b["compressor_type"]

            building_cooling_peak_load = data["building_cooling_peak_load"]
            target_chiller_type = (
                CHILLER_COMPRESSOR.SCREW
                if building_cooling_peak_load < REQUIRED_BUILDING_PEAK_LOAD_600
                else CHILLER_COMPRESSOR.CENTRIFUGAL
            )

            return {
                "compressor_type": compressor_type,
                "target_chiller_type": target_chiller_type,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            compressor_type = calc_vals["compressor_type"]
            target_chiller_type = calc_vals["target_chiller_type"]

            return compressor_type == target_chiller_type
