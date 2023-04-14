from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all


APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]


class Section19Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule14, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section19Rule14.HVACRule(),
            index_rmr="baseline",
            id="19-14",
            description="For baseline system types 1-8 and 11-13, if return or relief fans are specified in the proposed design, the baseline building design shall also be modeled with fans serving the same functions and sized for the baseline system supply fan air quantity less the minimum outdoor air, or 90% of the supply fan air quantity, whichever is larger.",
            ruleset_section_title="HVAC - General",
            standard_section="3.1.2.8.1 Excluding Exceptions 1 and 2",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )
    def create_data(self, context, data):

        return
    
    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict.keys()
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule14.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline

            return {}

        def rule_check(self, context, calc_vals=None, data=None):
            return ()
