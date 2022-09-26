from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.pint_utils import CalcQ
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
REQUIRED_TEMP_RANGE = ureg("10 degF")


class Section22Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule14, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule14.ChillerHeatRejectionRule(),
            index_rmr="baseline",
            id="22-14",
            description="The baseline heat-rejection device shall have a design temperature rise of 10°F.",
            rmr_context="ruleset_model_instances/0",
            list_path="heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11B": ["hvac_sys_11_b"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class ChillerHeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule14.ChillerHeatRejectionRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["range"],
                },
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.baseline
            heat_rejection_range = heat_rejection_b["range"]
            return {"heat_rejection_range": CalcQ("temperature", heat_rejection_range)}

        def rule_check(self, context, calc_vals=None, data=None):
            heat_rejection_range = calc_vals["heat_rejection_range"]
            return std_equal(
                heat_rejection_range.to(ureg.kelvin),
                REQUIRED_TEMP_RANGE.to(ureg.kelvin),
            )
