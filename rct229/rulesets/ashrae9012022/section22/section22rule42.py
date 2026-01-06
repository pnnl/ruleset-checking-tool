from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.does_chiller_performance_match_curve import (
    J4_CURVE,
    J6_CURVE,
    does_chiller_performance_match_curve,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_

ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]
CHILLER_COMPRESSOR = SchemaEnums.schema_enums["ChillerCompressorOptions"]

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


class PRM9012022Rule34d03(RuleDefinitionListIndexedBase):
    """Rule 42 of ASHRAE 90.1-2022 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012022Rule34d03, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012022Rule34d03.ChillerRule(),
            index_rmd=BASELINE_0,
            id="22-42",
            description="The sets of performance curves specified in Table J-2 should be used to represent part-load performance of chillers in the baseline building design.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.2.2.1 Baseline",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.chillers[*]",
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
        primary_secondary_loop_dict_b = get_primary_secondary_loops_dict(rmd_b)

        return {
            "primary_secondary_loop_dict_b": primary_secondary_loop_dict_b,
        }

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule34d03.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def is_applicable(self, context, data=None):
            chiller_b = context.BASELINE_0
            primary_secondary_loop_dict_b = data["primary_secondary_loop_dict_b"]

            return chiller_b["cooling_loop"] in primary_secondary_loop_dict_b

        def get_calc_vals(self, context, data=None):
            chiller_b = context.BASELINE_0

            rated_capacity_b = getattr_(chiller_b, "chillers", "rated_capacity")
            compressor_type_b = getattr_(chiller_b, "chillers", "compressor_type")

            # When 'curve_set_b' is None, there is a ValueError from the `does_chiller_performance_match_curve` function
            if compressor_type_b == CHILLER_COMPRESSOR.CENTRIFUGAL:
                if rated_capacity_b < 150 * ureg("ton"):
                    curve_set_b = J6_CURVE.Z
                elif 150 * ureg("ton") <= rated_capacity_b < 300 * ureg("ton"):
                    curve_set_b = J6_CURVE.AA
                else:
                    curve_set_b = J6_CURVE.AB
            elif compressor_type_b in (
                CHILLER_COMPRESSOR.POSITIVE_DISPLACEMENT,
                CHILLER_COMPRESSOR.SCROLL,
                CHILLER_COMPRESSOR.SCREW,
            ):
                if rated_capacity_b < 150 * ureg("ton"):
                    curve_set_b = J4_CURVE.V
                elif rated_capacity_b >= 300 * ureg("ton"):
                    curve_set_b = J6_CURVE.Y
                else:
                    curve_set_b = J6_CURVE.X

            return {"curve_set_b": curve_set_b}

        def rule_check(self, context, calc_vals=None, data=None):
            chiller_b = context.BASELINE_0
            curve_set_b = calc_vals["curve_set_b"]

            return does_chiller_performance_match_curve(chiller_b, curve_set_b)
