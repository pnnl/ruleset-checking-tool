from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_3_fns import table_g3_5_3_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

CHILLER_PART_LOAD_EFFICIENCY_METRIC = SchemaEnums.schema_enums[
    "ChillerPartLoadEfficiencyMetricOptions"
]

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


class Section22Rule32(RuleDefinitionListIndexedBase):
    """Rule 32 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule32, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule32.ChillerRule(),
            index_rmd=BASELINE_0,
            id="22-32",
            description="The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for part load, in accordance with Tables G3.5.3.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.2.1 Equipment Efficiencies",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="chillers[*]",
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

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule32.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                precision={
                    "chiller_part_load_efficiency": {
                        "precision": 0.001,
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.BASELINE_0
            rated_capacity_b = getattr_(chiller_b, "Chiller", "rated_capacity")
            compressor_type_b = getattr_(chiller_b, "Chiller", "compressor_type")
            chiller_part_load_efficiency = getattr_(
                chiller_b, "Chiller", "part_load_efficiency"
            ).to("Watt / Watt")
            part_load_efficiency_metric = getattr_(
                chiller_b, "Chiller", "part_load_efficiency_metric"
            )

            target_part_load_efficiency = table_g3_5_3_lookup(
                compressor_type_b, rated_capacity_b
            )["minimum_integrated_part_load"]

            return {
                "chiller_part_load_efficiency": CalcQ(
                    "cooling_efficiency", chiller_part_load_efficiency
                ),
                "target_part_load_efficiency": CalcQ(
                    "cooling_efficiency", target_part_load_efficiency
                ),
                "part_load_efficiency_metric": part_load_efficiency_metric,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            chiller_part_load_efficiency = calc_vals[
                "chiller_part_load_efficiency"
            ].magnitude
            target_part_load_efficiency = calc_vals["target_part_load_efficiency"]
            target_cop_part_load_efficiency = (
                1.0 / target_part_load_efficiency.to("kilowatt / kilowatt").magnitude
            )  # .magnitude is becuase `target_cop_part_load_efficiency` is still a `dimensionless` pint quantity
            part_load_efficiency_metric = calc_vals["part_load_efficiency_metric"]

            return (
                self.precision_comparison["chiller_part_load_efficiency"](
                    chiller_part_load_efficiency,
                    target_cop_part_load_efficiency,
                )
                and part_load_efficiency_metric
                == CHILLER_PART_LOAD_EFFICIENCY_METRIC.INTEGRATED_PART_LOAD_VALUE
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            chiller_part_load_efficiency = calc_vals["chiller_part_load_efficiency"]
            target_part_load_efficiency = calc_vals["target_part_load_efficiency"]
            target_cop_part_load_efficiency = 1.0 / target_part_load_efficiency.to(
                "kilowatt / kilowatt"
            )
            part_load_efficiency_metric = calc_vals["part_load_efficiency_metric"]

            return (
                std_equal(chiller_part_load_efficiency, target_cop_part_load_efficiency)
                and part_load_efficiency_metric
                == CHILLER_PART_LOAD_EFFICIENCY_METRIC.INTEGRATED_PART_LOAD_VALUE
            )
