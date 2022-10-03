from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-11.1",
    "SYS-11.2",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-11B",
    "SYS-12B",
    "SYS-13B",
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
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11": ["hvac_sys_11"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES and not found in NOT_APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule22.ChillerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["rated_capacity"],
                },
            )

        def get_calc_vals(self, context, data=None):
            chiller_b = context.baseline
            rated_capacity_b = chiller_b["rated_capacity"]
            compressor_type_b = chiller_b["compressor_type"]

            if rated_capacity_b < 150 * ureg("Btu/hr"):
                size_category = "< 150TONS"
            elif 150 * ureg("Btu/hr") <= rated_capacity_b < 300 * ureg("Btu/hr"):
                size_category = ">= 150TONS AND < 300TONS"
            elif 300 * ureg("Btu/hr") <= rated_capacity_b < 600 * ureg("Btu/hr"):
                size_category = ">= 300TONS AND < 600TONS"
            else:
                size_category = "> 600TONS"

            kW_ton_full_load_b = 1  ## should be replaced with table_3_2_lookup

            return {
                "size_category": size_category,
                "kW_ton_full_load_b": kW_ton_full_load_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            chiller_b = context.baseline
            full_load_efficiency_b = chiller_b["full_load_efficiency"]
            kW_ton_full_load_b = calc_vals["kW_ton_full_load_b"]
            return std_equal(full_load_efficiency_b, kW_ton_full_load_b * ureg(""))
