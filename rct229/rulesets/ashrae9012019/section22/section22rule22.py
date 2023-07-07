from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_3_fns import table_G3_5_3_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
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


class Section22Rule22(RuleDefinitionListIndexedBase):
    """Rule 22 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule22, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule22.ChillerRule(),
            index_rmr="baseline",
            id="22-22",
            description="The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for full load, in accordance with Tables G3.5.3.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.2.1 Equipment Efficiencies",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="chillers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
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
            super(Section22Rule22.ChillerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["compressor_type", "rated_capacity", "full_load_efficiency"],
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.baseline
            full_load_efficiency_b = chiller_b["full_load_efficiency"]

            compressor_type_b = chiller_b["compressor_type"]
            rated_capacity_b = chiller_b["rated_capacity"]

            required_kw_ton_full_load_b = table_G3_5_3_lookup(
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
            full_load_efficiency_b = calc_vals["full_load_efficiency_b"]
            required_kw_ton_full_load_b = calc_vals["required_kw_ton_full_load_b"]

            return std_equal(full_load_efficiency_b, required_kw_ton_full_load_b)
