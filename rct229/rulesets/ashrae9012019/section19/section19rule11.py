from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)


class PRM9012019Rule18u58(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule18u58, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule18u58.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-11",
            description="For systems that serve computer rooms, if the baseline system is HVAC System 11, it shall include an integrated fluid economizer meeting the requirements of Section 6.5.1.2 in the baseline building design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.6.1",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        return {"baseline_system_types_dict": get_baseline_system_types(rmd_b)}

    class HVACRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule18u58.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_b_id = hvac_b["id"]

            baseline_system_types_dict = data["baseline_system_types_dict"]
            system_type_b = next(
                (
                    key
                    for key, values in baseline_system_types_dict.items()
                    if hvac_b_id in values
                ),
                None,
            )

            does_hvac_system_match_b = baseline_system_type_compare(
                system_type_b, HVAC_SYS.SYS_11_1, False
            )

            return {"does_hvac_system_match_b": does_hvac_system_match_b}

        def applicability_check(self, context, calc_vals, data):
            does_hvac_system_match_b = calc_vals["does_hvac_system_match_b"]

            return does_hvac_system_match_b

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            return f"{hvac_id_b} was modeled as baseline system type 11-1, conduct a manual check that an integrated fluid economizer meeting the requirements of Section 6.5.1.2 was modeled in the baseline building design."
