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
from rct229.utils.assertions import assert_
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.schema.schema_enums import SchemaEnums

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

CHILLER_EFFICIENCY_METRIC_TYPES = SchemaEnums.schema_enums[
    "ChillerEfficiencyMetricOptions"
]


class PRM9012019Rule55f82(RuleDefinitionListIndexedBase):
    """Rule 22 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule55f82, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule55f82.ChillerRule(),
            index_rmd=BASELINE_0,
            id="22-22",
            description="The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for full load, in accordance with Tables G3.5.3.",
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
            super(PRM9012019Rule55f82.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": [
                        "compressor_type",
                        "rated_capacity",
                        "efficiency_metric_types",
                        "efficiency_metric_values",
                    ],
                },
                precision={
                    "full_load_efficiency_b": {
                        "precision": 0.1,
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.BASELINE_0
            compressor_type_b = chiller_b["compressor_type"]
            rated_capacity_b = chiller_b["rated_capacity"]
            efficiency_metric_types_b = chiller_b["efficiency_metric_types"]
            efficiency_metric_values_b = chiller_b["efficiency_metric_values"]

            assert_(
                len(efficiency_metric_types_b) == len(efficiency_metric_values_b)
                and 1 <= len(efficiency_metric_types_b) <= 5,
                "`efficiency_metric_types` and `efficiency_metric_values` must have the same length between 1 to 5",
            )

            full_load_efficiency_b = next(
                (
                    value.to("Watt / Watt")
                    for metric, value in zip(
                        efficiency_metric_types_b, efficiency_metric_values_b
                    )
                    if metric
                    == CHILLER_EFFICIENCY_METRIC_TYPES.FULL_LOAD_EFFICIENCY_RATED
                ),
                None,
            )

            assert_(
                full_load_efficiency_b is not None,
                "Baseline chiller `full_load_efficiency_b` should provided",
            )

            required_kw_ton_full_load_b = table_g3_5_3_lookup(
                compressor_type_b, rated_capacity_b
            )["minimum_full_load_efficiency"]

            return {
                "full_load_efficiency_b": CalcQ(
                    "cooling_efficiency", full_load_efficiency_b
                ),
                "required_kw_ton_full_load_b": CalcQ(
                    "cooling_efficiency", required_kw_ton_full_load_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            full_load_efficiency_b = calc_vals["full_load_efficiency_b"].magnitude
            required_kw_ton_full_load_b = calc_vals["required_kw_ton_full_load_b"]
            required_cop_full_load_b = (
                1.0 / required_kw_ton_full_load_b.to("kilowatt / kilowatt").magnitude
            )  # .magnitude is because `required_cop_full_load_b` is still a `dimensionless` pint quantify

            return self.precision_comparison["full_load_efficiency_b"](
                full_load_efficiency_b,
                required_cop_full_load_b,
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            full_load_efficiency_b = calc_vals["full_load_efficiency_b"]
            required_kw_ton_full_load_b = calc_vals["required_kw_ton_full_load_b"]
            required_cop_full_load_b = 1.0 / required_kw_ton_full_load_b.to(
                "kilowatt / kilowatt"
            )

            return std_equal(full_load_efficiency_b, required_cop_full_load_b)
