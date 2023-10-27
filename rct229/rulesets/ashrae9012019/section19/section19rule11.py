from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
]


class Section19Rule11((RuleDefinitionListIndexedBase)):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule11, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule11.HVACRule(),
            index_rmr="baseline",
            id="19-11",
            description="For systems that serve computer rooms, if the baseline system is HVAC System 11, it shall include an integrated fluid economizer meeting the requirements of Section 6.5.1.2 in the baseline building design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.6.1",
            is_primary_rule=False,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.baseline

        return {"baseline_system_types_dict": get_baseline_system_types(rmd_b)}

    class HVACRule(PartialRuleDefinition):
        def __init__(self):
            super(Section19Rule11.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            baseline_system_types_dict = data["baseline_system_types_dict"]

            does_baseline_sys_match_list_b = [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]

            return {"does_baseline_sys_match_list_b": does_baseline_sys_match_list_b}

        def applicability_check(self, context, calc_vals, data):
            does_baseline_sys_match_list_b = calc_vals["does_baseline_sys_match_list_b"]

            return any(does_baseline_sys_match_list_b)

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]

            return f"{hvac_id_b} was modeled as baseline system type 11-1, conduct a manual check that an integrated fluid economizer meeting the requirements of Section 6.5.1.2 was modeled in the baseline building design."
