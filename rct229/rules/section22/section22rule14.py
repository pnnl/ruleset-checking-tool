from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
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
REQUIRED_TEMP_RANGE = ureg("10 degF")


class Section22Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule14, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule14.HeatRejectionRule(),
            index_rmr="baseline",
            id="22-14",
            description="The baseline heat-rejection device shall have a design temperature rise of 10°F.",
            rmr_context="ruleset_model_instances/0",
            list_path="heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_type_lists = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_lists
            ]
        )

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule14.HeatRejectionRule, self).__init__(
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
