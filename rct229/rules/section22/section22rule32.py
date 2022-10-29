from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_5_3_fns import table_G3_5_3_lookup
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.assertions import getattr_
from rct229.utils.std_comparisons import std_equal

CHILLER_PART_LOAD_EFFICIENCY_METRIC = schema_enums[
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
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule32.ChillerRule(),
            index_rmr="baseline",
            id="22-32",
            description="The baseline chiller efficiencies shall be modeled at the "
            "minimum efficiency levels for part load, in accordance with Tables G3.5.3.",
            rmr_context="ruleset_model_instances/0",
            list_path="chillers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types = get_baseline_system_types(rmi_b)
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [
                sys_type in APPLICABLE_SYS_TYPES
                for sys_type in baseline_system_types.keys()
            ]
        )

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule32.ChillerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.baseline
            rated_capacity_b = getattr_(chiller_b, "Chiller", "rated_capacity")
            compressor_type_b = getattr_(chiller_b, "Chiller", "compressor_type")
            part_load_efficiency = getattr_(
                chiller_b, "Chiller", "part_load_efficiency"
            )
            part_load_efficiency_metric = getattr_(
                chiller_b, "Chiller", "part_load_efficiency_metric"
            )
            # TODO: What does "IPLV" mean in the RDS - it doesn't seem to be needed for the lookup
            # TODO: Is this a good variable name for the lookup result?
            target_part_load_efficiency = table_G3_5_3_lookup(
                compressor_type_b, rated_capacity_b
            )

            return {
                "part_load_efficiency": part_load_efficiency,
                "target_part_load_efficiency": target_part_load_efficiency,
                "part_load_efficiency_metric": part_load_efficiency_metric,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            chiller_part_load_efficiency = calc_vals["chiller_part_load_efficiency"]
            target_part_load_efficiency = calc_vals["target_part_load_efficiency"]
            part_load_efficiency_metric = calc_vals["part_load_efficiency_metric"]

            return (
                std_equal(chiller_part_load_efficiency, target_part_load_efficiency)
                and part_load_efficiency_metric
                == CHILLER_PART_LOAD_EFFICIENCY_METRIC.INTEGRATED_PART_LOAD_VALUE
            )
