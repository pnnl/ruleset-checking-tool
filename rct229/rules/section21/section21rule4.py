from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_12A,
]
BOILER_COMBUSTION_OPTION = schema_enums["BoilerCombustionOptions"]


class Section21Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule4, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule4.BoilerRule(),
            index_rmr="baseline",
            id="21-4",
            description="When baseline building does not use purchased heat, baseline systems 1,5,7,11,12 shall be modeled with natural draft boilers.",
            rmr_context="ruleset_model_instances/0",
            list_path="boilers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types = get_baseline_system_types(rmi_b)
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class BoilerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule4.BoilerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["draft_type"],
                },
            )

        def get_calc_vals(self, context, data=None):
            boiler_b = context.baseline
            boiler_draft_type_b = boiler_b["draft_type"]
            return {"boiler_draft_type_b": boiler_draft_type_b}

        def rule_check(self, context, calc_vals=None, data=None):
            boiler_draft_type_b = calc_vals["boiler_draft_type_b"]
            return boiler_draft_type_b == BOILER_COMBUSTION_OPTION.NATURAL
